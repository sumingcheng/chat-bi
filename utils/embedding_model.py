import httpx
from backend.config.app_config import Config


def get_text_embedding(text):
    """
    使用 Ollama 部署的模型获取文本嵌入向量
    """
    try:
        with httpx.Client(verify=False) as client:
            response = client.post(
                Config.EMBEDDING_API_URL,
                json={
                    "model": Config.EMBEDDING_MODEL,
                    "prompt": text,
                },
            )
            response.raise_for_status()
            result = response.json()
            return result["embedding"]
    except Exception as e:
        raise Exception(f"获取文本嵌入向量失败: {e}")
