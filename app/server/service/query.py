import json
import logging
import uuid
from decimal import Decimal
from typing import Dict, Any, List, Optional

from app.common.milvus_client import milvus_client
from app.common.embedding_client import get_text_embedding
from app.common.parameter_resolver import ParameterResolver
from app.common.visualization import suggest_visualization_type
from app.common.utils import convert_to_serializable, ensure_sql_limit
from app.database.validation import validate_sql_query, sanitize_sql_query
from app.database.repository import BusinessRepository, SystemRepository
from app.agent.chat_bi_agent import ChatBIAgent

logger = logging.getLogger(__name__)


async def query_db_sql(
    user_question: str, session_id: Optional[str] = None
) -> Dict[str, Any]:
    """Chat-BI 核心查询接口"""
    query_id = str(uuid.uuid4())[:12]

    try:
        logger.info(f"开始处理查询 {query_id}: {user_question}")

        # embedding 现在是异步调用
        user_embedding = await get_text_embedding(user_question)

        matched_template = await search_similar_template(user_embedding)

        sql_params = {}
        if matched_template:
            logger.info(f"匹配到SQL模板: {matched_template['description']}")
            final_sql, sql_params = await fill_template_with_parameters(
                user_question,
                matched_template["sql_text"],
                matched_template.get("required_params", []),
            )
        else:
            logger.info("未匹配到合适模板，使用AI生成SQL")
            final_sql = await ChatBIAgent.generate_sql(user_question)

        validate_sql_query(final_sql)
        final_sql = sanitize_sql_query(final_sql)
        final_sql = ensure_sql_limit(final_sql)

        query_result = await BusinessRepository.execute_query(final_sql, sql_params)
        viz_type = suggest_visualization_type(query_result)
        answer = await ChatBIAgent.generate_answer(user_question, query_result)

        # 新 SQL 成功执行后存为模板
        if not matched_template and query_result:
            await ChatBIAgent.save_template(user_question, final_sql, user_embedding)

        serializable_result = convert_to_serializable(query_result)
        await SystemRepository.save_query_history(
            query_id=query_id,
            user_input=user_question,
            sql_query=final_sql,
            result=json.dumps(serializable_result, ensure_ascii=False),
            visualization_type=viz_type,
        )

        logger.info(f"查询 {query_id} 处理完成，返回 {len(query_result)} 条记录")

        return {
            "success": True,
            "data": {
                "query_id": query_id,
                "answer": answer,
                "chart_data": {
                    "type": viz_type,
                    "data": serializable_result,
                    "config": generate_chart_config(viz_type, query_result),
                },
                "sql": final_sql,
                "record_count": len(query_result),
            },
            "message": "查询成功",
        }

    except Exception as e:
        logger.error(f"查询 {query_id} 处理失败: {e}")
        await SystemRepository.save_query_history(
            query_id=query_id, user_input=user_question, result=f"查询失败: {str(e)}"
        )
        return {
            "success": False,
            "data": {},
            "error": {"code": 500, "message": f"查询处理失败: {str(e)}"},
        }


async def search_similar_template(
    user_embedding: List[float],
) -> Optional[Dict[str, Any]]:
    """在 Milvus 中搜索相似 SQL 模板"""
    try:
        if not milvus_client.has_collection("sql_templates"):
            return None

        collection = milvus_client.get_collection("sql_templates")
        search_results = collection.search(
            data=[user_embedding],
            anns_field="embedding",
            param={"metric_type": "COSINE", "params": {"nprobe": 10}},
            limit=1,
            output_fields=[
                "template_id", "description", "sql_text",
                "scenario", "required_params",
            ],
        )

        if search_results[0] and len(search_results[0]) > 0:
            best_match = search_results[0][0]
            if best_match.score > 0.7:
                return {
                    "template_id": best_match.entity.get("template_id"),
                    "description": best_match.entity.get("description"),
                    "sql_text": best_match.entity.get("sql_text"),
                    "scenario": best_match.entity.get("scenario"),
                    "required_params": json.loads(
                        best_match.entity.get("required_params", "[]")
                    ),
                    "similarity": best_match.score,
                }

        return None

    except Exception as e:
        logger.error(f"Milvus搜索失败: {e}")
        return None


async def fill_template_with_parameters(
    user_question: str, sql_template: str, required_params: List[str]
) -> str:
    """提取参数并填充 SQL 模板，使用参数化方式防注入"""
    if not required_params:
        return sql_template, {}

    try:
        params, ambiguities = await ParameterResolver.resolve_parameters(
            user_question, required_params
        )
        if ambiguities:
            logger.warning(f"参数解析存在歧义: {ambiguities}")

        # 将 {param} 占位符转为 :param 格式，通过 SQLAlchemy 参数化执行防注入
        parameterized_sql = sql_template
        for param_name in required_params:
            parameterized_sql = parameterized_sql.replace(
                f"{{{param_name}}}", f":{param_name}"
            )

        # 把参数值附加到 SQL 元数据中，后续 execute_query 会使用
        return parameterized_sql, params

    except Exception as e:
        logger.error(f"模板参数填充失败: {e}")
        return sql_template, {}


def generate_chart_config(viz_type: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """生成图表配置"""
    if not data:
        return {}

    columns = list(data[0].keys())
    config = {"title": "数据可视化", "columns": columns}
    numeric_columns = [col for col in columns if _is_numeric_column(data, col)]
    dimension_columns = [col for col in columns if col not in numeric_columns]

    # 中文注释：优先挑业务语义更强的字段，而不是盲目按列位置猜
    preferred_numeric = _pick_numeric_column(numeric_columns)
    preferred_dimension = _pick_dimension_column(dimension_columns)

    if viz_type in ("bar", "line"):
        config.update({
            "xField": preferred_dimension or (columns[0] if columns else ""),
            "yField": preferred_numeric or (columns[1] if len(columns) > 1 else ""),
        })
    elif viz_type == "pie":
        config.update({
            "angleField": preferred_numeric or (columns[1] if len(columns) > 1 else ""),
            "colorField": preferred_dimension or (columns[0] if columns else ""),
        })

    return config


def _is_numeric_column(data: List[Dict[str, Any]], column: str) -> bool:
    values = [row.get(column) for row in data]
    non_null_values = [value for value in values if value is not None]
    return bool(non_null_values) and all(isinstance(value, (int, float, Decimal)) for value in non_null_values)


def _pick_numeric_column(columns: List[str]) -> str:
    priority_keywords = ["percentage", "percent", "ratio", "rate", "share", "amount", "sales", "total", "count", "qty", "quantity"]
    return _pick_column_by_keywords(columns, priority_keywords)


def _pick_dimension_column(columns: List[str]) -> str:
    priority_keywords = ["name", "category", "type", "status", "date", "time", "month", "day"]
    return _pick_column_by_keywords(columns, priority_keywords)


def _pick_column_by_keywords(columns: List[str], keywords: List[str]) -> str:
    for keyword in keywords:
        for column in columns:
            if keyword in column.lower():
                return column
    return columns[0] if columns else ""
