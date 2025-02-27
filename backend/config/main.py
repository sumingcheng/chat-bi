import os


class Config:
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 13306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "chat-bi")

    MILVUS_HOST = os.getenv("MILVUS_HOST", "localhost")
    MILVUS_PORT = os.getenv("MILVUS_PORT", "19530")

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    EMBEDDING_API_URL = os.getenv(
        "EMBEDDING_API_URL", "http://172.22.220.64:11434/api/embeddings"
    )
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "bge-m3")

    required_vars = ["DB_USER", "DB_PASSWORD", "DB_NAME", "OPENAI_API_KEY"]
    for var in required_vars:
        if locals()[var] is None:
            raise ValueError(f"环境变量 {var} 未设置。")

    @classmethod
    def as_dict(cls):
        # 敏感的配置项名称
        sensitive_keys = {"DB_PASSWORD", "OPENAI_API_KEY"}
        return {
            k: v
            for k, v in cls.__dict__.items()
            if not k.startswith("__") and not callable(v) and k not in sensitive_keys
        }
