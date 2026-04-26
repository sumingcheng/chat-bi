from decimal import Decimal
from typing import List, Dict, Any


def _is_numeric_column(data: List[Dict[str, Any]], column: str) -> bool:
    values = [row.get(column) for row in data]
    non_null_values = [value for value in values if value is not None]
    return bool(non_null_values) and all(isinstance(value, (int, float, Decimal)) for value in non_null_values)


def suggest_visualization_type(data: List[Dict[str, Any]]) -> str:
    """
    基于查询结果推荐合适的可视化类型
    """
    if not data:
        return "table"

    # 获取数据的列
    columns = list(data[0].keys())

    numeric_columns = [col for col in columns if _is_numeric_column(data, col)]
    dimension_columns = [col for col in columns if col not in numeric_columns]

    # 占比/百分比字段优先使用饼图，语义比柱状图更稳定
    percentage_columns = [
        col
        for col in numeric_columns
        if any(keyword in col.lower() for keyword in ["percentage", "percent", "ratio", "rate", "share"])
    ]
    if percentage_columns and dimension_columns:
        return "pie"

    # 如果只有两列数据，且其中一列是数值类型
    if len(columns) == 2 and len(numeric_columns) == 1:
        return "pie"

    # 如果有时间相关的列，可能适合折线图
    time_related_columns = [
        col
        for col in columns
        if any(
            keyword in col.lower()
            for keyword in ["time", "date", "year", "month", "day"]
        )
    ]
    if time_related_columns and len(columns) > 1:
        return "line"

    # 有维度列 + 数值列时，优先柱状图
    if numeric_columns and dimension_columns:
        return "bar"

    # 默认使用表格
    return "table"
