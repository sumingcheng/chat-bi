import re
import openai
from openai import OpenAIError
from backend.utils.prompts import database_schema
from backend.journal.logging import logger
from backend.config.main import Config
from backend.utils.retry import with_retry


@with_retry(max_retries=3, delay=1.0, exceptions=(OpenAIError,))
async def call_openai_api(messages: list, **kwargs) -> str:
    """
    带重试机制的OpenAI API调用
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=messages,
            temperature=0,
            **kwargs
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        logger.error(f"OpenAI API 调用失败: {e}")
        raise


async def parse_query_to_sql(user_query: str) -> str:
    """
    将用户查询解析为SQL查询
    """
    openai.api_key = Config.OPENAI_API_KEY

    messages = [
        {
            "role": "system",
            "content": f"""
                你是一个将自然语言查询直接转换为针对 MySQL 数据库的 SQL 查询的专家。
                请只返回 SQL 查询，并保证 SQL 语句是正确的，数据库使用的是 only_full_group_by 模式。
                \n\n数据库DDL如下：\n{database_schema()}
                要求：
                - 查询应包含必要的表关联
                - SELECT 子句中应包括所有相关字段
                - 确保语法正确，可在 MySQL 中执行
            """,
        },
        {
            "role": "user",
            "content": f'请将以下问题转换为SQL查询: "{user_query}"',
        },
    ]

    logger.info(f"用户问题：{user_query}")
    
    raw_response = await call_openai_api(messages, max_tokens=150)
    logger.info(f"原始 OpenAI 响应: {raw_response}")

    # 提取SQL查询
    sql_query = raw_response
    if "```" in raw_response:
        matches = re.findall(r"```(?:sql)?\s*(.*?)\s*```", raw_response, re.DOTALL)
        if matches:
            sql_query = matches[0].strip()
    else:
        select_index = raw_response.lower().find("select")
        if select_index != -1:
            sql_query = raw_response[select_index:].strip()

    logger.info(f"提取的 SQL 查询: {sql_query}")
    return sql_query
