from typing import Any

import httpx

from app.config.app_config import Config


LLM_PROVIDER_ORDER = ("openai", "deepseek")

_runtime_provider: str | None = None
_runtime_model: str | None = None


def _provider_config(provider: str) -> dict[str, Any]:
    config = Config.get_llm_provider_config(provider)
    if not config:
        raise ValueError(f"不支持的 LLM provider: {provider}")
    return config


def _default_selection() -> tuple[str, str]:
    if _runtime_provider and _runtime_model:
        return _runtime_provider, _runtime_model

    provider = _runtime_provider or (
        Config.LLM_PROVIDER if Config.LLM_PROVIDER in Config.LLM_PROVIDERS else "openai"
    )
    config = _provider_config(provider)
    if config.get("api_key"):
        return provider, _runtime_model or Config.LLM_MODEL or str(config.get("default_model"))

    for provider in LLM_PROVIDER_ORDER:
        config = _provider_config(provider)
        if config.get("api_key"):
            return provider, str(config.get("default_model"))

    raise ValueError("没有可用的 LLM provider，请先配置 api_key")


def get_active_selection() -> dict[str, str]:
    provider, model = _default_selection()
    return {"provider": provider, "model": model}


def get_active_provider_config() -> dict[str, str]:
    selection = get_active_selection()
    config = _provider_config(selection["provider"])
    if not config.get("api_key"):
        raise ValueError(f"LLM provider 未配置 api_key: {selection['provider']}")

    return {
        "provider": selection["provider"],
        "model": selection["model"],
        "api_key": str(config["api_key"]),
        "base_url": str(config["base_url"]),
    }


def list_providers() -> list[dict[str, Any]]:
    selection = get_active_selection()
    providers = []

    for provider in LLM_PROVIDER_ORDER:
        config = _provider_config(provider)
        providers.append({
            "provider": provider,
            "name": config.get("name", provider),
            "configured": bool(config.get("api_key")),
            "base_url": config.get("base_url"),
            "default_model": config.get("default_model"),
            "active": provider == selection["provider"],
        })

    return providers


async def list_models(provider: str) -> list[str]:
    config = _provider_config(provider)
    api_key = config.get("api_key")
    if not api_key:
        raise ValueError(f"LLM provider 未配置 api_key: {provider}")

    base_url = str(config.get("base_url")).rstrip("/")
    async with httpx.AsyncClient(verify=False, timeout=30) as client:
        response = await client.get(
            f"{base_url}/models",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        response.raise_for_status()
        payload = response.json()

    models = [
        item.get("id")
        for item in payload.get("data", [])
        if item.get("id")
    ]
    return sorted(models)


def set_active_selection(provider: str, model: str) -> dict[str, str]:
    global _runtime_provider, _runtime_model

    if not model:
        raise ValueError("model 不能为空")

    config = _provider_config(provider)
    if not config.get("api_key"):
        raise ValueError(f"LLM provider 未配置 api_key: {provider}")

    _runtime_provider = provider
    _runtime_model = model
    return get_active_selection()
