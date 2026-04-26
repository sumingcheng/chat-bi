import logging
from pymilvus import connections, Collection, CollectionSchema, FieldSchema, DataType, utility
from app.config.app_config import Config

logger = logging.getLogger(__name__)

EMBEDDING_DIM = Config.EMBEDDING_DIM
COLLECTION_NAME = "sql_templates"


class MilvusClient:
    """Milvus 连接管理"""

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
        try:
            connections.disconnect(alias="default")
            self._is_connected = False
            logger.info("已断开 Milvus 连接")
        except Exception as e:
            logger.error(f"断开 Milvus 连接失败: {e}")

    def is_connected(self):
        return self._is_connected

    def get_collection(self, collection_name: str):
        if not self._is_connected:
            raise RuntimeError("Milvus 未连接")
        if not utility.has_collection(collection_name):
            raise ValueError(f"集合 '{collection_name}' 不存在")
        return Collection(collection_name)

    def has_collection(self, collection_name: str):
        if not self._is_connected:
            raise RuntimeError("Milvus 未连接")
        return utility.has_collection(collection_name)

    def list_collections(self):
        if not self._is_connected:
            raise RuntimeError("Milvus 未连接")
        return utility.list_collections()

    def ensure_template_collection(self) -> Collection:
        """确保 sql_templates collection 存在，不存在则创建"""
        if not self._is_connected:
            raise RuntimeError("Milvus 未连接")

        if utility.has_collection(COLLECTION_NAME):
            collection = Collection(COLLECTION_NAME)
            collection.load()
            return collection

        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="template_id", dtype=DataType.INT64),
            FieldSchema(name="description", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="sql_text", dtype=DataType.VARCHAR, max_length=4096),
            FieldSchema(name="scenario", dtype=DataType.VARCHAR, max_length=256),
            FieldSchema(name="required_params", dtype=DataType.VARCHAR, max_length=1024),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=EMBEDDING_DIM),
        ]
        schema = CollectionSchema(fields, description="SQL 模板向量库")
        collection = Collection(COLLECTION_NAME, schema)

        # 创建向量索引
        collection.create_index(
            field_name="embedding",
            index_params={
                "metric_type": "COSINE",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 128},
            },
        )
        collection.load()
        logger.info(f"创建 Milvus 集合: {COLLECTION_NAME}")
        return collection


milvus_client = MilvusClient()
