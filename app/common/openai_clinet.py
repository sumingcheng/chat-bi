import logging
import httpx
from openai import AsyncOpenAI
from openai import OpenAIError
from app.config.app_config import Config

logger = logging.getLogger(__name__)

client = AsyncOpenAI(
    api_key=Config.OPENAI_API_KEY,
    base_url="https://api.deepseek.com",
    http_client=httpx.AsyncClient(verify=False),
)


async def call_openai_api(messages: list, **kwargs) -> str:
    try:
        response = await client.chat.completions.create(
            model="deepseek-reasoner", messages=messages, temperature=0, **kwargs
        )
        return response.choices[0].message.content.strip()
    except OpenAIError as e:
        logger.error(f"OpenAI API 调用失败: {e}")
        raise
