from backend.utils.openai import parse_query_to_sql
from backend.database.sql_validation import validate_sql_query
from backend.database.mysql import execute_sql_query
from backend.utils.milvus import (
    connect_milvus,
    get_or_create_collection,
    insert_data,
    search_similar_question,
)
from backend.handlers.template_matcher import match_sql_template
from backend.utils.visualization import suggest_visualization_type
from backend.journal.logging import logger
from backend.utils.cache import QueryCache
from backend.utils.parameter_resolver import ParameterResolver
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models import QueryHistory
import json
import uuid

# 创建缓存实例
query_cache = QueryCache()


async def process_query(user_input: str, db: AsyncSession) -> dict:
    try:
        # 1. 尝试从缓存获取结果
        cached_result = await query_cache.get(user_input)
        if cached_result:
            logger.info("使用缓存的查询结果")
            return cached_result

        sql_query = None

        # 2. 首先尝试从Milvus中搜索相似问题
        connect_milvus()
        collection = get_or_create_collection()
        search_results = search_similar_question(collection, user_input)

        if search_results and len(search_results[0]) > 0:
            top_hit = search_results[0][0]
            if top_hit.score > 0.9:
                sql_query = top_hit.entity.get("sql_query")
                logger.info(f"使用相似问题的SQL查询: {sql_query}")

        # 3. 如果没有找到相似问题，尝试模板匹配
        if not sql_query:
            template_result = match_sql_template(user_input)
            if template_result:
                template_sql, raw_params = template_result

                # 处理参数歧义
                resolver = ParameterResolver()
                params, ambiguities = await resolver.resolve_parameters(
                    user_input, list(raw_params.keys())
                )
                resolved_params, conflicts = await resolver.resolve_parameter_conflicts(
                    params, ambiguities
                )

                if conflicts:
                    logger.warning(f"参数存在歧义: {conflicts}")

                sql_query = template_sql.format(**resolved_params)
                logger.info(f"使用模板生成的SQL查询: {sql_query}")

        # 4. 如果模板也没匹配上，使用OpenAI生成SQL
        if not sql_query:
            sql_query = await parse_query_to_sql(user_input)
            logger.info(f"使用OpenAI生成的SQL查询: {sql_query}")

        # 验证SQL安全性
        validate_sql_query(sql_query)

        # 执行查询
        result = execute_sql_query(sql_query)

        # 格式化数据并推荐可视化类型
        formatted_data = format_for_echarts(result)
        visualization_type = suggest_visualization_type(formatted_data)

        # 保存查询记录
        query_history = QueryHistory(
            query_id=str(uuid.uuid4()),
            user_input=user_input,
            sql_query=sql_query,
            result=json.dumps(formatted_data)
        )
        db.add(query_history)
        await db.commit()

        # 缓存结果
        response = {
            "data": formatted_data,
            "visualization_type": visualization_type,
            "sql_query": sql_query,
        }
        await query_cache.set(user_input, response)

        return response

    except Exception as e:
        logger.error(f"处理查询失败: {e}")
        raise


# 将结果格式化为 echarts 可用的数据格式
def format_for_echarts(data):
    columns = data["columns"]
    rows = data["data"]
    echarts_data = [dict(zip(columns, row)) for row in rows]
    return echarts_data
