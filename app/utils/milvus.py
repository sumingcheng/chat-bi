from app.journal.logging import logger
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility
from app.utils.embedding_model import get_text_embedding
from config.main import Config


# 连接到 Milvus
def connect_milvus():
    host = Config.MILVUS_HOST
    port = Config.MILVUS_PORT
    connections.connect(alias='default', host=host, port=port)


# 检查集合是否存在
def has_collection(name):
    return utility.has_collection(name)


def create_index(collection):
    index_params = {
        "metric_type": "COSINE",
        "index_type": "IVF_FLAT",
        "params": {"nlist": 128}
    }
    collection.create_index(field_name="embedding", index_params=index_params)


def get_or_create_collection():
    collection_name = 'question_embedding_collection'

    if not utility.has_collection(collection_name):
        # 定义字段
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="question", dtype=DataType.VARCHAR, max_length=512),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=1536),
            FieldSchema(name="sql_query", dtype=DataType.VARCHAR, max_length=2048)
        ]
        schema = CollectionSchema(fields, description="Question embeddings")
        collection = Collection(collection_name, schema=schema)

        # 创建索引，没有索引的向量搜索会非常慢。创建索引可以显著提高搜索性能
        create_index(collection)
    else:
        collection = Collection(collection_name)
        # **检查并创建索引**
        if not collection.has_index():
            create_index(collection)
        else:
            logger.info(f"集合 {collection_name} 已存在索引：{collection.indexes}")

    # 加载集合和索引
    collection.load()
    return collection


# 插入数据
def insert_data(collection, questions, sql_queries):
    embeddings = []
    valid_questions = []
    valid_sql_queries = []

    for q, sql in zip(questions, sql_queries):
        try:
            embedding = get_text_embedding(q)
            embeddings.append(embedding)
            valid_questions.append(q)
            valid_sql_queries.append(sql)
        except Exception as e:
            logger.error(f"获取文本嵌入时出错：{e}")
            continue

    data = [
        valid_questions,
        embeddings,
        valid_sql_queries
    ]

    collection.insert(data)
    collection.load()


# 搜索相似问题
def search_similar_question(collection, user_question, top_k=1):
    # 直接加载集合
    collection.load()

    # 生成用户问题的嵌入向量
    user_embedding = get_text_embedding(user_question)
    user_embedding = [user_embedding]

    # 执行向量搜索
    search_params = {
        "metric_type": "COSINE",
        "params": {
            "nprobe": 10  # 取 nlist 的 1% 到 10%。
        }
    }

    results = collection.search(
        data=user_embedding,
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        expr=None,
        output_fields=["question", "sql_query"]
    )

    return results
