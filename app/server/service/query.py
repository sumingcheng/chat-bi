import json
import logging
import uuid
from typing import Dict, Any, List, Optional
from app.common.milvus_client import milvus_client
from app.common.embedding_client import get_text_embedding
from app.common.parameter_resolver import ParameterResolver
from app.common.openai_clinet import call_openai_api
from app.common.visualization import suggest_visualization_type
from app.database.validation import validate_sql_query, sanitize_sql_query
from app.database.repository import BusinessRepository, SystemRepository
from app.agent.parse_query_to_sql import parse_query_to_sql

logger = logging.getLogger(__name__)


async def query_db_sql(
    user_question: str, session_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Chat-BI 核心查询接口

    Args:
        user_question: 用户自然语言问题
        session_id: 可选的会话ID

    Returns:
        包含答案、可视化数据和SQL的响应
    """
    query_id = str(uuid.uuid4())[:12]  # 生成12位短UUID

    try:
        logger.info(f"开始处理查询 {query_id}: {user_question}")

        # 1. 向量化用户问题
        user_embedding = get_text_embedding(user_question)
        logger.debug("用户问题向量化完成")

        # 2. Milvus 相似度检索最佳SQL模板
        matched_template = await search_similar_template(user_embedding, user_question)

        if matched_template:
            logger.info(f"匹配到SQL模板: {matched_template['description']}")

            # 3. 参数提取和填充模板
            final_sql = await fill_template_with_parameters(
                user_question,
                matched_template["sql_text"],
                matched_template.get("required_params", []),
            )
        else:
            logger.info("未匹配到合适模板，使用AI生成SQL")

            # 4. AI生成SQL（带数据库Schema上下文）
            final_sql = await generate_sql_with_context(user_question)

        # 5. SQL安全检查
        validate_sql_query(final_sql)
        final_sql = sanitize_sql_query(final_sql)

        # 6. 执行SQL查询
        query_result = await BusinessRepository.execute_query(final_sql)

        # 7. 推荐可视化类型
        viz_type = suggest_visualization_type(query_result)

        # 8. 生成自然语言答案
        answer = await generate_natural_answer(user_question, query_result)

        # 9. 如果是新生成的SQL，存储为模板
        if not matched_template and query_result:
            await store_new_template(user_question, final_sql, user_embedding)

        # 10. 保存查询历史
        await SystemRepository.save_query_history(
            query_id=query_id,
            user_input=user_question,
            sql_query=final_sql,
            result=json.dumps(query_result, ensure_ascii=False),
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
                    "data": query_result,
                    "config": generate_chart_config(viz_type, query_result),
                },
                "sql": final_sql,
                "record_count": len(query_result),
            },
            "message": "查询成功",
        }

    except Exception as e:
        logger.error(f"查询 {query_id} 处理失败: {e}")

        # 保存失败的查询历史
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
    """
    在Milvus中搜索相似的SQL模板
    """
    try:
        if not milvus_client.has_collection("sql_templates"):
            logger.warning("Milvus中不存在sql_templates集合")
            return None

        collection = milvus_client.get_collection("sql_templates")

        # 向量相似度搜索
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

            # 相似度阈值判断
            if similarity_score > 0.7:  # 可调整阈值
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
    """
    提取参数并填充SQL模板
    """
    try:
        if not required_params:
            return sql_template

        # 使用参数解析器提取参数
        params, ambiguities = await ParameterResolver.resolve_parameters(
            user_question, required_params
        )

        if ambiguities:
            logger.warning(f"参数解析存在歧义: {ambiguities}")

        # 填充模板
        filled_sql = sql_template
        for param_name, param_value in params.items():
            placeholder = f"{{{param_name}}}"
            filled_sql = filled_sql.replace(placeholder, str(param_value))

        return filled_sql

    except Exception as e:
        logger.error(f"参数填充失败: {e}")
        raise


async def generate_sql_with_context(user_question: str) -> str:
    """
    带数据库Schema上下文的AI SQL生成
    """
    try:
        # 获取数据库Schema信息
        schema_info = await BusinessRepository.get_database_schema()

        # 构建Schema描述
        schema_desc = build_schema_description(schema_info)

        prompt = f"""
        你是一个SQL专家。基于以下数据库Schema信息，将用户问题转换为SQL查询。

        数据库Schema:
        {schema_desc}

        用户问题: {user_question}

        要求:
        1. 只返回SQL查询语句，不要任何解释
        2. 使用标准MySQL语法
        3. 确保查询的安全性，只能是SELECT语句
        4. 如果需要JOIN，请使用表之间的外键关系
        5. 对于时间相关查询，假设当前时间为NOW()
        
        SQL查询:
        """

        sql_response = await call_openai_api(
            [
                {"role": "system", "content": "你是一个SQL查询专家，只返回SQL语句。"},
                {"role": "user", "content": prompt},
            ]
        )

        # 清理响应，提取纯SQL
        sql_query = extract_sql_from_response(sql_response)

        return sql_query

    except Exception as e:
        logger.error(f"AI SQL生成失败: {e}")
        raise


def build_schema_description(schema_info: Dict[str, Any]) -> str:
    """
    构建数据库Schema的文本描述
    """
    description = "数据库表结构:\n\n"

    for table in schema_info.get("tables", []):
        table_name = table["table_name"]
        table_comment = table.get("table_comment", "")

        description += f"表名: {table_name}"
        if table_comment:
            description += f" ({table_comment})"
        description += "\n"

        for column in table.get("columns", []):
            col_name = column["column_name"]
            col_type = column["data_type"]
            col_comment = column.get("column_comment", "")
            is_key = column.get("column_key", "")

            description += f"  - {col_name} ({col_type})"
            if is_key == "PRI":
                description += " [主键]"
            elif is_key == "MUL":
                description += " [外键]"
            if col_comment:
                description += f" // {col_comment}"
            description += "\n"
        description += "\n"

    # 添加外键关系描述
    if schema_info.get("relationships"):
        description += "表关系:\n"
        for rel in schema_info["relationships"]:
            description += f"  {rel['table_name']}.{rel['column_name']} -> {rel['referenced_table_name']}.{rel['referenced_column_name']}\n"

    return description


def extract_sql_from_response(response: str) -> str:
    """
    从AI响应中提取纯SQL语句
    """
    # 移除可能的markdown代码块标记
    response = response.strip()
    if response.startswith("```sql"):
        response = response[6:]
    elif response.startswith("```"):
        response = response[3:]

    if response.endswith("```"):
        response = response[:-3]

    # 移除多余的空白和换行
    response = response.strip()

    return response


async def generate_natural_answer(
    user_question: str, query_result: List[Dict[str, Any]]
) -> str:
    """
    基于查询结果生成自然语言答案
    """
    try:
        if not query_result:
            return "根据您的查询条件，没有找到相关数据。"

        # 构建结果摘要
        result_summary = f"查询返回了 {len(query_result)} 条记录。"

        # 如果结果较少，可以具体描述
        if len(query_result) <= 5:
            sample_data = json.dumps(query_result[:3], ensure_ascii=False, indent=2)
        else:
            sample_data = json.dumps(query_result[:2], ensure_ascii=False, indent=2)

        prompt = f"""
        用户问题: {user_question}
        
        查询结果摘要: {result_summary}
        样本数据: {sample_data}
        
        请基于查询结果，用自然语言回答用户的问题。要求:
        1. 语言简洁明了
        2. 突出关键数据
        3. 如果有多条记录，给出总体概况
        4. 用中文回答
        """

        answer = await call_openai_api(
            [
                {
                    "role": "system",
                    "content": "你是一个数据分析助手，根据查询结果回答用户问题。",
                },
                {"role": "user", "content": prompt},
            ]
        )

        return answer

    except Exception as e:
        logger.error(f"生成自然语言答案失败: {e}")
        return f"查询成功，共找到 {len(query_result)} 条相关记录。"


async def store_new_template(
    user_question: str, sql_query: str, user_embedding: List[float]
):
    """
    将新生成的SQL存储为模板
    """
    try:
        # 生成模板描述
        description = await generate_template_description(user_question, sql_query)

        # 提取SQL中的参数（简单实现）
        required_params = extract_sql_parameters(sql_query)

        # 存储到系统数据库
        template_data = {
            "description": description,
            "sql_text": sql_query,
            "scenario": "auto_generated",
            "required_params": json.dumps(required_params),
        }

        # 这里可以调用SystemRepository保存模板
        logger.info(f"存储新SQL模板: {description}")

        # TODO: 存储到Milvus向量数据库
        # 需要实现向Milvus插入新的模板向量

    except Exception as e:
        logger.error(f"存储新模板失败: {e}")


async def generate_template_description(user_question: str, sql_query: str) -> str:
    """
    为SQL模板生成描述
    """
    try:
        prompt = f"""
        用户问题: {user_question}
        SQL查询: {sql_query}
        
        请为这个SQL查询生成一个简洁的功能描述，用于将来的模板匹配。
        描述应该:
        1. 概括查询的主要目的
        2. 突出查询的业务场景
        3. 长度控制在50字以内
        4. 使用中文
        """

        description = await call_openai_api(
            [
                {
                    "role": "system",
                    "content": "你是一个SQL分析专家，为SQL查询生成简洁描述。",
                },
                {"role": "user", "content": prompt},
            ]
        )

        return description.strip()

    except Exception as e:
        logger.error(f"生成模板描述失败: {e}")
        return f"基于用户问题生成的查询: {user_question[:30]}..."


def extract_sql_parameters(sql_query: str) -> List[str]:
    """
    从SQL中提取参数占位符（简单实现）
    """
    import re

    # 查找形如 {param_name} 的参数占位符
    pattern = r"\{(\w+)\}"
    matches = re.findall(pattern, sql_query)

    return list(set(matches))  # 去重


def generate_chart_config(viz_type: str, data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    为不同图表类型生成配置
    """
    if not data:
        return {}

    columns = list(data[0].keys())

    config = {"title": "查询结果", "responsive": True}

    if viz_type == "bar":
        config.update(
            {
                "xAxis": columns[0] if columns else "",
                "yAxis": columns[1] if len(columns) > 1 else "",
                "orientation": "vertical",
            }
        )
    elif viz_type == "line":
        config.update(
            {
                "xAxis": columns[0] if columns else "",
                "yAxis": columns[1] if len(columns) > 1 else "",
                "smooth": True,
            }
        )
    elif viz_type == "pie":
        config.update(
            {
                "labelField": columns[0] if columns else "",
                "valueField": columns[1] if len(columns) > 1 else "",
                "showLegend": True,
            }
        )
    elif viz_type == "table":
        config.update({"columns": columns, "pagination": len(data) > 20})

    return config
