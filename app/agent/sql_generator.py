import logging
from typing import Dict, Any, List
from app.common.openai_clinet import call_openai_api
from app.database.repository import BusinessRepository

logger = logging.getLogger(__name__)


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