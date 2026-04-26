import logging

import httpx
from app.config.app_config import Config

logger = logging.getLogger(__name__)


async def get_text_embedding(text: str) -> list[float]:
    """统一的 Embedding 入口，根据 EMBEDDING_PROVIDER 路由"""
    provider = Config.EMBEDDING_PROVIDER.lower()
    if provider == "openai":
        return await _openai_embedding(text)
    elif provider == "ollama":
        return await _ollama_embedding(text)
    else:
        raise ValueError(f"不支持的 EMBEDDING_PROVIDER: {provider}")


async def _openai_embedding(text: str) -> list[float]:
    """OpenAI Embedding API"""
    from openai import AsyncOpenAI

    client = AsyncOpenAI(
        api_key=Config.EMBEDDING_API_KEY,
        base_url=Config.get_embedding_base_url(),
    )
    response = await client.embeddings.create(
        model=Config.EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding


async def _ollama_embedding(text: str) -> list[float]:
    """Ollama 本地 Embedding API"""
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(
            Config.EMBEDDING_API_URL,
            json={"model": Config.EMBEDDING_MODEL, "prompt": text},
        )
        response.raise_for_status()
        return response.json()["embedding"]
