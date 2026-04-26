import logging

import httpx
from openai import AsyncOpenAI, OpenAIError
from app.common.llm_registry import get_active_provider_config

logger = logging.getLogger(__name__)


def _supports_temperature(model: str) -> bool:
    return not model.startswith("gpt-5.5")


async def call_llm(messages: list, **kwargs) -> str:
    """统一的 LLM 调用入口，provider 通过配置切换"""
    active_config = get_active_provider_config()
    model = kwargs.pop("model", active_config["model"])
    client = AsyncOpenAI(
        api_key=active_config["api_key"],
        base_url=active_config["base_url"],
        http_client=httpx.AsyncClient(verify=False),
    )

    try:
        temperature = kwargs.pop("temperature", None)
        request_kwargs = {
            "model": model,
            "messages": messages,
            **kwargs,
        }

        # gpt-5.5 只接受默认 temperature，强传 0 会 400
        if _supports_temperature(model):
            request_kwargs["temperature"] = 0 if temperature is None else temperature

        response = await client.chat.completions.create(
            **request_kwargs,
        )
        return response.choices[0].message.content.strip()

    except OpenAIError as e:
        logger.error(f"LLM 调用失败 [provider={active_config['provider']}, model={model}]: {e}")
        raise
    finally:
        await client.close()
