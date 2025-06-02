from typing import List, Dict, Any


def suggest_visualization_type(data: List[Dict[str, Any]]) -> str:
    """
    基于查询结果推荐合适的可视化类型
    """
    if not data:
        return "table"

    # 获取数据的列
    columns = list(data[0].keys())

    # 如果只有两列数据，且其中一列是数值类型
    if len(columns) == 2:
        numeric_values = [isinstance(data[0][col], (int, float)) for col in columns]
        if sum(numeric_values) == 1:
            return "pie"  # 饼图适合显示占比

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

    # 如果有多个数值列，使用柱状图
    numeric_columns = [
        col
        for col in columns
        if all(isinstance(row[col], (int, float)) for row in data)
    ]
    if len(numeric_columns) > 0:
        return "bar"

    # 默认使用表格
    return "table"
