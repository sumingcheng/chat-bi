import requests
from config.main import Config

EMBEDDING_API_URL = "http://172.22.220.64:11434/api/embeddings"


def get_text_embedding(text):
    """
    使用 Ollama 部署的 bge-m3 模型获取文本嵌入向量
    """
    try:
        response = requests.post(
            EMBEDDING_API_URL,
            json={
                "model": "bge-m3",
                "prompt": text,
            },
        )
        response.raise_for_status()
        result = response.json()
        return result["embedding"]
    except Exception as e:
        raise Exception(f"获取文本嵌入向量失败: {e}")
