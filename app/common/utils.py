import re
from decimal import Decimal
from datetime import date, datetime, time
from typing import Any


def convert_to_serializable(obj: Any) -> Any:
    """递归转换不可 JSON 序列化的类型"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, (date, datetime)):
        return obj.isoformat()
    elif isinstance(obj, time):
        return obj.strftime('%H:%M:%S')
    elif isinstance(obj, dict):
        return {key: convert_to_serializable(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_to_serializable(item) for item in obj)
    return obj


def extract_sql_from_response(response: str) -> str:
    """从 AI 响应中提取纯 SQL 语句，去除 markdown 代码块标记"""
    response = response.strip()
    if response.startswith("```sql"):
        response = response[6:]
    elif response.startswith("```"):
        response = response[3:]
    if response.endswith("```"):
        response = response[:-3]
    return response.strip()


def extract_sql_parameters(sql_query: str) -> list[str]:
    """从 SQL 中提取 {param} 占位符"""
    matches = re.findall(r"\{(\w+)\}", sql_query)
    return list(set(matches))


def ensure_sql_limit(sql: str, max_rows: int = 1000) -> str:
    """确保 SQL 包含 LIMIT，防止全表扫描拖垮服务"""
    upper = sql.upper().strip()
    if "LIMIT" not in upper:
        sql = sql.rstrip().rstrip(";")
        sql += f" LIMIT {max_rows}"
    return sql
