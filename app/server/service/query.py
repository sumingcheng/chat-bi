import json
import logging
import uuid
from decimal import Decimal
from typing import Dict, Any, List, Optional
from app.common.milvus_client import milvus_client
from app.common.embedding_client import get_text_embedding
from app.common.parameter_resolver import ParameterResolver
from app.common.visualization import suggest_visualization_type
from app.database.validation import validate_sql_query, sanitize_sql_query
from app.database.repository import BusinessRepository, SystemRepository
from app.agent.chat_bi_agent import ChatBIAgent

logger = logging.getLogger(__name__)


def convert_decimals_to_float(obj: Any) -> Any:
    """递归转换Decimal为float"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {key: convert_decimals_to_float(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimals_to_float(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_decimals_to_float(item) for item in obj)
    else:
        return obj


async def query_db_sql(
    user_question: str, session_id: Optional[str] = None
) -> Dict[str, Any]:
    """Chat-BI核心查询接口"""
    query_id = str(uuid.uuid4())[:12]

    try:
        logger.info(f"开始处理查询 {query_id}: {user_question}")

        user_embedding = get_text_embedding(user_question)
        logger.debug("用户问题向量化完成")

        matched_template = await search_similar_template(user_embedding, user_question)

        if matched_template:
            logger.info(f"匹配到SQL模板: {matched_template['description']}")

            final_sql = await fill_template_with_parameters(
                user_question,
                matched_template["sql_text"],
                matched_template.get("required_params", []),
            )
        else:
            logger.info("未匹配到合适模板，使用AI生成SQL")

            final_sql = await ChatBIAgent.generate_sql(user_question)

        validate_sql_query(final_sql)
        final_sql = sanitize_sql_query(final_sql)

        query_result = await BusinessRepository.execute_query(final_sql)

        viz_type = suggest_visualization_type(query_result)

        answer = await ChatBIAgent.generate_answer(user_question, query_result)

        if not matched_template and query_result:
            await ChatBIAgent.save_template(user_question, final_sql, user_embedding)

        serializable_result = convert_decimals_to_float(query_result)
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
                    "data": convert_decimals_to_float(query_result),
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
    user_embedding: List[float], user_question: str
) -> Optional[Dict[str, Any]]:
    """在Milvus中搜索相似SQL模板"""
    try:
        if not milvus_client.has_collection("sql_templates"):
            logger.warning("Milvus中不存在sql_templates集合")
            return None

        collection = milvus_client.get_collection("sql_templates")

        search_results = collection.search(
            data=[user_embedding],
            anns_field="embedding",
            param={"metric_type": "COSINE", "params": {"nprobe": 10}},
            limit=1,
            output_fields=[
                "template_id",
                "description",
                "sql_text",
                "scenario",
                "required_params",
            ],
        )

        if search_results[0] and len(search_results[0]) > 0:
            best_match = search_results[0][0]
            similarity_score = best_match.score

            if similarity_score > 0.7:
                return {
                    "template_id": best_match.entity.get("template_id"),
                    "description": best_match.entity.get("description"),
                    "sql_text": best_match.entity.get("sql_text"),
                    "scenario": best_match.entity.get("scenario"),
                    "required_params": json.loads(
                        best_match.entity.get("required_params", "[]")
                    ),
                    "similarity": similarity_score,
                }

        return None

    except Exception as e:
        logger.error(f"Milvus搜索失败: {e}")
        return None


async def fill_template_with_parameters(
    user_question: str, sql_template: str, required_params: List[str]
) -> str:
    """提取参数并填充SQL模板"""
    try:
        if not required_params:
            return sql_template

        params, ambiguities = await ParameterResolver.resolve_parameters(
            user_question, required_params
        )

        if ambiguities:
            logger.warning(f"参数解析存在歧义: {ambiguities}")

        filled_sql = sql_template
        for param_name, param_value in params.items():
            placeholder = f"{{{param_name}}}"
            filled_sql = filled_sql.replace(placeholder, str(param_value))

        return filled_sql

    except Exception as e:
        logger.error(f"模板参数填充失败: {e}")
        return sql_template


def generate_chart_config(viz_type: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """生成图表配置"""
    if not data:
        return {}

    columns = list(data[0].keys())
    
    config = {
        "title": "数据可视化",
        "columns": columns
    }
    
    if viz_type == "bar":
        config.update({
            "xField": columns[0] if columns else "",
            "yField": columns[1] if len(columns) > 1 else "",
        })
    elif viz_type == "line":
        config.update({
            "xField": columns[0] if columns else "",
            "yField": columns[1] if len(columns) > 1 else "",
        })
    elif viz_type == "pie":
        config.update({
            "angleField": columns[1] if len(columns) > 1 else "",
            "colorField": columns[0] if columns else "",
        })
    
    return config
