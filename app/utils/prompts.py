import json
import os
from typing import Optional, Dict, Any


def database_schema(table_name: Optional[str] = None) -> str:
    """
    根据表名返回对应的 DDL 信息

    参数:
        table_name: 可选，表名。如果不提供，则返回所有表的 DDL 信息

    返回:
        str: 表的 DDL 信息或所有表的 DDL 信息
    """
    # 获取 db_ddl.json 文件的路径
    current_dir = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    ddl_path = os.path.join(current_dir, "bin", "db_ddl.json")

    try:
        # 读取 JSON 文件
        with open(ddl_path, 'r', encoding='utf-8') as f:
            ddl_data = json.load(f)

        tables_info = ddl_data.get("tables", {})

        # 如果没有指定表名，返回所有表的 DDL
        if table_name is None:
            result = []
            for table, info in tables_info.items():
                result.append(f"表名: {table}\n{info.get('ddl', '')}\n")
            return "\n".join(result)

        # 如果指定了表名，返回该表的 DDL
        if table_name in tables_info:
            return tables_info[table_name].get("ddl", "")
        else:
            return f"未找到表 '{table_name}' 的 DDL 信息"

    except Exception as e:
        return f"获取 DDL 信息时出错: {str(e)}"


def get_database_tables() -> Dict[str, Any]:
    """
    获取数据库中所有表的信息

    返回:
        Dict: 包含所有表信息的字典
    """
    current_dir = os.path.dirname(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    ddl_path = os.path.join(current_dir, "bin", "db_ddl.json")

    try:
        with open(ddl_path, 'r', encoding='utf-8') as f:
            ddl_data = json.load(f)
        return ddl_data.get("tables", {})
    except Exception:
        return {}
