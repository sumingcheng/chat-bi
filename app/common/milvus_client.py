import logging
from pymilvus import connections, Collection, utility
from app.config.app_config import Config

logger = logging.getLogger(__name__)


class MilvusClient:
    """Milvus 连接池客户端"""

    _instance = None
    _is_connected = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MilvusClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._is_connected:
            self.connect()

    def connect(self):
        """连接到 Milvus"""
        try:
            host = Config.MILVUS_HOST
            port = Config.MILVUS_PORT
            connections.connect(alias="default", host=host, port=port)
            self._is_connected = True
            logger.info(f"成功连接到 Milvus: {host}:{port}")
        except Exception as e:
            logger.error(f"连接 Milvus 失败: {e}")
            raise

    def disconnect(self):
        """断开连接"""
        try:
            connections.disconnect(alias="default")
            self._is_connected = False
            logger.info("已断开 Milvus 连接")
        except Exception as e:
            logger.error(f"断开 Milvus 连接失败: {e}")

    def is_connected(self):
        """检查连接状态"""
        return self._is_connected

    def get_collection(self, collection_name: str):
        """获取集合实例"""
        if not self._is_connected:
            raise RuntimeError("Milvus 未连接")

        if not utility.has_collection(collection_name):
            raise ValueError(f"集合 '{collection_name}' 不存在")

        return Collection(collection_name)

    def has_collection(self, collection_name: str):
        """检查集合是否存在"""
        if not self._is_connected:
            raise RuntimeError("Milvus 未连接")

        return utility.has_collection(collection_name)

    def list_collections(self):
        """列出所有集合"""
        if not self._is_connected:
            raise RuntimeError("Milvus 未连接")

        return utility.list_collections()


# 单例实例
milvus_client = MilvusClient()
