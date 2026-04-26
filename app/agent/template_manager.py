import json
import logging
from typing import List

from app.common.llm_client import call_llm
from app.common.milvus_client import milvus_client
from app.common.utils import extract_sql_parameters
from app.database.base import get_system_session
from app.database.system_models import SQLTemplate, SQLTemplateParam

logger = logging.getLogger(__name__)


async def store_new_template(
    user_question: str, sql_query: str, user_embedding: List[float]
):
    """将新生成的 SQL 存储为模板，同时写入 MySQL 和 Milvus"""
    try:
        description = await generate_template_description(user_question, sql_query)
        required_params = extract_sql_parameters(sql_query)

        # 写入 MySQL
        template_id = await _save_template_to_mysql(
            description, sql_query, required_params
        )

        # 写入 Milvus
        _save_template_to_milvus(
            template_id, description, sql_query, required_params, user_embedding
        )

        logger.info(f"模板存储完成 [id={template_id}]: {description}")

    except Exception as e:
        logger.error(f"存储新模板失败: {e}")


async def _save_template_to_mysql(
    description: str, sql_query: str, required_params: List[str]
) -> int:
    """写入 MySQL，返回 template_id"""
    async for session in get_system_session():
        template = SQLTemplate(
            description=description,
            sql_text=sql_query,
            scenario="auto_generated",
        )
        session.add(template)
        await session.flush()

        for param_name in required_params:
            param = SQLTemplateParam(
                template_id=template.id,
                param_name=param_name,
                param_type="string",
            )
            session.add(param)

        await session.commit()
        return template.id


def _save_template_to_milvus(
    template_id: int,
    description: str,
    sql_query: str,
    required_params: List[str],
    embedding: List[float],
):
    """写入 Milvus 向量库"""
    collection = milvus_client.ensure_template_collection()
    collection.insert([
        [template_id],
        [description[:500]],
        [sql_query[:4000]],
        ["auto_generated"],
        [json.dumps(required_params)],
        [embedding],
    ])
    collection.flush()


async def generate_template_description(user_question: str, sql_query: str) -> str:
    """为 SQL 模板生成简洁描述"""
    try:
        prompt = f"""
        用户问题: {user_question}
        SQL查询: {sql_query}
        
        请为这个SQL查询生成一个简洁的功能描述，用于将来的模板匹配。
        
        **严格要求：**
        1. 概括查询的主要目的
        2. 突出查询的业务场景
        3. 长度控制在50字以内
        4. 使用中文
        5. 只返回纯文本描述，不要任何格式化标记或解释
        """
        description = await call_llm([
            {"role": "system", "content": "你是一个SQL分析专家，为SQL查询生成简洁描述。只返回纯文本，不要任何格式化。"},
            {"role": "user", "content": prompt},
        ])
        return description.strip()

    except Exception as e:
        logger.error(f"生成模板描述失败: {e}")
        return f"基于用户问题生成的查询: {user_question[:30]}..."
