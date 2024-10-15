import os
from .logging_config import logger
import mysql.connector


# 数据库连接
def get_db_connection():
    connection = mysql.connector.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        port=int(os.getenv('DB_PORT', 13306)),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', ''),
        database=os.getenv('DB_NAME', 'chat-bi')
    )
    return connection


# 执行 SQL 查询并返回结果
def execute_sql_query(sql_query):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        logger.info(f"执行 SQL 查询: {sql_query}")
        cursor.execute(sql_query)
        columns = cursor.column_names
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return {"columns": columns, "data": results}
    except mysql.connector.Error as err:
        logger.error(f"数据库错误: {err}")
        raise ValueError("数据库查询失败。")
