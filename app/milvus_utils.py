from .logging_config import logger
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection
import os
from .embedding_model import get_text_embedding


# 连接到 Milvus
def connect_milvus():
    host = os.getenv('MILVUS_HOST', 'localhost')
    port = os.getenv('MILVUS_PORT', '19530')
    connections.connect(alias='default', host=host, port=port)


# 检查集合是否存在
def has_collection(name):
    return Collection.exists(name)


# 创建或获取集合
def get_or_create_collection():
    collection_name = 'question_embedding_collection'
    if not has_collection(collection_name):
        # 定义字段
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
            FieldSchema(name="sql_query", dtype=DataType.VARCHAR, max_length=2048)
        ]
        schema = CollectionSchema(fields, description="Question embeddings")
        collection = Collection(collection_name, schema)
    else:
        collection = Collection(collection_name)
    return collection


# 插入数据
def insert_data(collection, questions, sql_queries):
    embeddings = []
    for q in questions:
        try:
            embedding = get_text_embedding(q)
            embeddings.append(embedding)
        except Exception as e:
            logger.error(f"获取文本嵌入时出错：{e}")
            # 可以选择跳过该条数据或终止
            raise e
    data = [
        questions,
        embeddings,
        sql_queries
    ]
    collection.insert(data)
    collection.load()


# 搜索相似问题
def search_similar_question(collection, user_question, top_k=1):
    # 生成用户问题的嵌入向量
    user_embedding = get_text_embedding(user_question)
    user_embedding = [user_embedding]  # 转换为列表，以匹配 search 接口的输入格式

    # 执行向量搜索
    search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}

    results = collection.search(
        data=user_embedding,
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        expr=None,
        output_fields=["question", "sql_query"]
    )

    return results
