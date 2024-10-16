from app.journal.logging import logger
import mysql.connector

from config.main import Config


# 数据库连接
def get_db_connection():
    connection = mysql.connector.connect(
        host=Config.DB_HOST,
        port=int(Config.DB_PORT),
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        database=Config.DB_NAME
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
