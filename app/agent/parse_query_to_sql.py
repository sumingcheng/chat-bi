import logging
from app.common.openai_clinet import call_openai_api

logger = logging.getLogger(__name__)


async def parse_query_to_sql(user_prompt: str, schema_context: str = "") -> str:
    """将用户自然语言问题转换为SQL查询"""
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
        
        response = await call_openai_api([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        response = response.strip()
        if response.startswith("```sql"):
            response = response[6:]
        elif response.startswith("```"):
            response = response[3:]
        if response.endswith("```"):
            response = response[:-3]
        response = response.strip()
        
        return response
        
    except Exception as e:
        logger.error(f"SQL生成失败: {e}")
        raise
