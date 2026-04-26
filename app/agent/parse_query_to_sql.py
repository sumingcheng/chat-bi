import logging

from app.common.llm_client import call_llm
from app.common.utils import extract_sql_from_response

logger = logging.getLogger(__name__)


async def parse_query_to_sql(user_prompt: str, schema_context: str = "") -> str:
    """将用户自然语言问题转换为 SQL 查询（带 schema 上下文）"""
    try:
        system_prompt = f"""
        你是一个SQL查询专家，请将用户的自然语言问题转换为SQL查询语句。
        
        数据库Schema信息:
        {schema_context}
        
        **严格要求：**
        1. 仅返回SQL查询语句，不要返回任何解释、注释或说明
        2. 使用标准MySQL语法
        3. 确保查询的安全性，只能是SELECT语句
        4. 不要使用```sql```代码块标记
        5. 直接输出纯SQL语句
        """

        response = await call_llm([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ])

        return extract_sql_from_response(response)

    except Exception as e:
        logger.error(f"SQL生成失败: {e}")
        raise
