from openai import OpenAI
import openai
from openai import OpenAIError
from utils.prompts import database_schema
from journal.logging import logger
from config.main import Config
from utils.retry import with_retry

client = OpenAI(api_key=Config.OPENAI_API_KEY)


@with_retry(max_retries=3, delay=1.0, exceptions=(OpenAIError,))
async def call_openai_api(messages: list, **kwargs) -> str:
    """
    带重试机制的OpenAI API调用
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4", messages=messages, temperature=0, **kwargs
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        logger.error(f"OpenAI API 调用失败: {e}")
        raise


async def parse_query_to_sql(query: str) -> str:
    """
    使用OpenAI将自然语言查询转换为SQL
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个SQL专家，请将用户的自然语言问题转换为SQL查询语句。",
                },
                {"role": "user", "content": query},
            ],
            temperature=0,
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API调用失败: {e}")
        raise


def get_openai_client():
    """
    获取OpenAI客户端实例
    """
    return client
