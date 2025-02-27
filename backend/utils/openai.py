from openai import OpenAI
from openai import OpenAIError
from journal.logging import logger
from config.main import Config
import httpx

client = OpenAI(
    api_key=Config.OPENAI_API_KEY,
    base_url="https://api.deepseek.com",
    http_client=httpx.Client(verify=False),
)


async def call_openai_api(messages: list, **kwargs) -> str:
    try:
        response = client.chat.completions.create(
            model="deepseek-chat", messages=messages, temperature=0, **kwargs
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        logger.error(f"OpenAI API 调用失败: {e}")
        raise


async def parse_query_to_sql(query: str) -> str:
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个SQL查询专家，请将用户的自然语言问题转换为SQL查询语句。仅返回SQL查询语句，不要返回任何解释或说明。",
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
    return client
