import os
from pathlib import Path

import yaml

# 项目根目录
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_CONFIG_PATH = _PROJECT_ROOT / "config.yaml"

_PROVIDER_BASE_URLS = {
    "openai": "https://api.openai.com/v1",
    "deepseek": "https://api.deepseek.com",
}


def _load_yaml() -> dict:
    """加载 YAML 配置文件，不存在则返回空字典"""
    if _CONFIG_PATH.exists():
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {}


def _get(yaml_cfg: dict, yaml_path: str, env_key: str, default=None):
    """YAML 为主，环境变量覆盖"""
    env_val = os.getenv(env_key)
    if env_val is not None:
        return env_val

    keys = yaml_path.split(".")
    node = yaml_cfg
    for k in keys:
        if isinstance(node, dict):
            node = node.get(k)
        else:
            return default
    return node if node is not None else default


_cfg = _load_yaml()


class Config:
    DEBUG = str(_get(_cfg, "debug", "DEBUG", "false")).lower() in ("true", "1", "yes")

    # MySQL
    DB_HOST = str(_get(_cfg, "database.host", "DB_HOST", "localhost"))
    DB_PORT = int(_get(_cfg, "database.port", "DB_PORT", 3306))
    DB_USER = str(_get(_cfg, "database.user", "DB_USER", "root"))
    DB_PASSWORD = str(_get(_cfg, "database.password", "DB_PASSWORD", ""))
    DB_NAME = str(_get(_cfg, "database.name", "DB_NAME", "chat_bi"))
    DB_SYS_NAME = str(_get(_cfg, "database.sys_name", "DB_SYS_NAME", "chat_bi_system"))

    # Milvus
    MILVUS_HOST = str(_get(_cfg, "milvus.host", "MILVUS_HOST", "localhost"))
    MILVUS_PORT = str(_get(_cfg, "milvus.port", "MILVUS_PORT", "19530"))

    # LLM
    LLM_PROVIDER = str(_get(_cfg, "llm.provider", "LLM_PROVIDER", "openai"))
    LLM_MODEL = str(_get(_cfg, "llm.model", "LLM_MODEL", "gpt-4.1"))
    _LEGACY_LLM_API_KEY = str(_get(_cfg, "llm.api_key", "LLM_API_KEY", "") or "")
    LLM_BASE_URL = str(_get(_cfg, "llm.base_url", "LLM_BASE_URL", "") or "")
    LLM_PROVIDERS = {
        "openai": {
            "name": "OpenAI",
            "base_url": str(_get(_cfg, "llm.providers.openai.base_url", "OPENAI_BASE_URL", "") or _PROVIDER_BASE_URLS["openai"]),
            "api_key": str(
                _get(_cfg, "llm.providers.openai.api_key", "OPENAI_API_KEY", "")
                or (_LEGACY_LLM_API_KEY if LLM_PROVIDER == "openai" else "")
            ),
            "default_model": str(
                _get(_cfg, "llm.providers.openai.model", "OPENAI_MODEL", "")
                or (LLM_MODEL if LLM_PROVIDER == "openai" else "gpt-5-chat-latest")
            ),
        },
        "deepseek": {
            "name": "DeepSeek",
            "base_url": str(_get(_cfg, "llm.providers.deepseek.base_url", "DEEPSEEK_BASE_URL", "") or _PROVIDER_BASE_URLS["deepseek"]),
            "api_key": str(
                _get(_cfg, "llm.providers.deepseek.api_key", "DEEPSEEK_API_KEY", "")
                or (_LEGACY_LLM_API_KEY if LLM_PROVIDER == "deepseek" else "")
            ),
            "default_model": str(
                _get(_cfg, "llm.providers.deepseek.model", "DEEPSEEK_MODEL", "")
                or (LLM_MODEL if LLM_PROVIDER == "deepseek" else "deepseek-reasoner")
            ),
        },
    }
    LLM_API_KEY = str(LLM_PROVIDERS.get(LLM_PROVIDER, {}).get("api_key", "") or _LEGACY_LLM_API_KEY)

    # Embedding
    EMBEDDING_PROVIDER = str(_get(_cfg, "embedding.provider", "EMBEDDING_PROVIDER", "openai"))
    EMBEDDING_MODEL = str(_get(_cfg, "embedding.model", "EMBEDDING_MODEL", "text-embedding-3-small"))
    EMBEDDING_DIM = int(_get(_cfg, "embedding.dim", "EMBEDDING_DIM", 1536))
    EMBEDDING_API_KEY = str(_get(_cfg, "embedding.api_key", "EMBEDDING_API_KEY", "") or LLM_API_KEY)
    EMBEDDING_API_URL = str(_get(_cfg, "embedding.api_url", "EMBEDDING_API_URL", "") or "")

    # 向后兼容
    OPENAI_API_KEY = LLM_API_KEY

    @classmethod
    def get_llm_base_url(cls) -> str:
        if cls.LLM_BASE_URL:
            return cls.LLM_BASE_URL
        provider = cls.LLM_PROVIDERS.get(cls.LLM_PROVIDER, {})
        return str(provider.get("base_url") or _PROVIDER_BASE_URLS.get(cls.LLM_PROVIDER, "https://api.openai.com/v1"))

    @classmethod
    def get_llm_provider_config(cls, provider: str) -> dict:
        return dict(cls.LLM_PROVIDERS.get(provider, {}))

    @classmethod
    def get_configured_llm_providers(cls) -> list[str]:
        return [
            provider
            for provider, config in cls.LLM_PROVIDERS.items()
            if config.get("api_key")
        ]

    @classmethod
    def get_embedding_base_url(cls) -> str:
        return _PROVIDER_BASE_URLS.get("openai", "https://api.openai.com/v1")

    # 启动校验
    if not DB_PASSWORD:
        raise ValueError("database.password 未设置")
    if not any(config.get("api_key") for config in LLM_PROVIDERS.values()):
        raise ValueError("至少需要配置一个 llm provider api_key")

    @classmethod
    def as_dict(cls):
        sensitive = {"DB_PASSWORD", "OPENAI_API_KEY", "LLM_API_KEY", "LLM_PROVIDERS", "EMBEDDING_API_KEY"}
        return {
            k: v for k, v in cls.__dict__.items()
            if not k.startswith("_") and not callable(v) and k not in sensitive
        }
