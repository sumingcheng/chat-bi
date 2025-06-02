import logging
from app.common.openai_clinet import call_openai_api

logger = logging.getLogger(__name__)


async def parse_query_to_sql(user_prompt: str, schema_context: str = "") -> str:
    """
    将用户自然语言问题转换为SQL查询
    
    Args:
        user_prompt: 用户问题
        schema_context: 数据库Schema上下文
        
    Returns:
        SQL查询语句
    """
    try:
        system_prompt = f"""
        你是一个SQL查询专家，请将用户的自然语言问题转换为SQL查询语句。
        
        数据库Schema信息:
        {schema_context}
        
        要求:
        1. 仅返回SQL查询语句，不要返回任何解释或说明
        2. 使用标准MySQL语法
        3. 确保查询的安全性，只能是SELECT语句
        """
        
        response = await call_openai_api([
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ])
        
        return response
        
    except Exception as e:
        logger.error(f"SQL生成失败: {e}")
        raise


user_prompt = "请查询所有用户"
