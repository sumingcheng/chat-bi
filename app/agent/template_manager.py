import json
import logging
from typing import List
from app.common.openai_clinet import call_openai_api

logger = logging.getLogger(__name__)


async def store_new_template(
    user_question: str, sql_query: str, user_embedding: List[float]
):
    """将新生成的SQL存储为模板"""
    try:
        description = await generate_template_description(user_question, sql_query)
        required_params = extract_sql_parameters(sql_query)

        template_data = {
            "description": description,
            "sql_text": sql_query,
            "scenario": "auto_generated",
            "required_params": json.dumps(required_params),
        }

        logger.info(f"存储新SQL模板: {description}")

    except Exception as e:
        logger.error(f"存储新模板失败: {e}")


async def generate_template_description(user_question: str, sql_query: str) -> str:
    """为SQL模板生成描述"""
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

        description = await call_openai_api(
            [
                {
                    "role": "system",
                    "content": "你是一个SQL分析专家，为SQL查询生成简洁描述。只返回纯文本，不要任何格式化。",
                },
                {"role": "user", "content": prompt},
            ]
        )

        return description.strip()

    except Exception as e:
        logger.error(f"生成模板描述失败: {e}")
        return f"基于用户问题生成的查询: {user_question[:30]}..."


def extract_sql_parameters(sql_query: str) -> List[str]:
    """从SQL中提取参数占位符"""
    import re

    pattern = r"\{(\w+)\}"
    matches = re.findall(pattern, sql_query)

    return list(set(matches)) 