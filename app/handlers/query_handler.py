from app.utils.openai import parse_query_to_sql
from app.database.sql_validation import validate_sql_query
from app.database.mysql import execute_sql_query
from app.utils.milvus import connect_milvus, get_or_create_collection, insert_data, search_similar_question
from app.journal.logging import logger


def process_query(user_input):
    try:
        # 连接到 Milvus 并获取集合
        connect_milvus()
        collection = get_or_create_collection()

        # 搜索相似问题
        search_results = search_similar_question(collection, user_input)
        logger.debug(f"搜索结果: {search_results}")

        if search_results and len(search_results[0]) > 0:
            top_hit = search_results[0][0]
            if top_hit.score > 0.8:
                # 使用相似问题的 SQL 查询
                sql_query = top_hit.entity.get("sql_query")
                logger.info(f"使用相似问题的 SQL 查询: {sql_query}")
            else:
                logger.info("未找到高相似度的问题，将处理新问题。")
                # 处理新问题
                sql_query = parse_query_to_sql(user_input)
                validate_sql_query(sql_query)
                # 将新问题和 SQL 查询添加到知识库中
                insert_data(collection, [user_input], [sql_query])
        else:
            logger.info("未找到相似的问题，将处理新问题。")
            # 没有搜索到任何结果，处理新问题
            sql_query = parse_query_to_sql(user_input)
            validate_sql_query(sql_query)
            # 将新问题和 SQL 查询添加到知识库中
            insert_data(collection, [user_input], [sql_query])

        data = execute_sql_query(sql_query)
        echarts_data = format_for_echarts(data)
        return {"echarts_data": echarts_data}

    except Exception as e:
        logger.error(f"处理查询 '{user_input}' 时出错: {e}")
        # 抛出异常，由调用者处理
        raise e


# 将结果格式化为 echarts 可用的数据格式
def format_for_echarts(data):
    columns = data['columns']
    rows = data['data']
    echarts_data = {
        'columns': columns,
        'rows': [list(row) for row in rows]
    }
    return echarts_data
