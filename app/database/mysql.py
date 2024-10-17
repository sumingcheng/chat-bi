from app.journal.logging import logger
from config.main import Config
import mysql.connector

dbconfig = {
    "host": Config.DB_HOST,
    "port": int(Config.DB_PORT),
    "user": Config.DB_USER,
    "password": Config.DB_PASSWORD,
    "database": Config.DB_NAME
}

pool_name = "mysql_pool"
pool_size = 5
# 创建连接池
pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name=pool_name,
    pool_size=pool_size,
    **dbconfig
)


# 从连接池获取连接
def get_db_connection():
    try:
        connection = pool.get_connection()
        return connection
    except Exception as e:
        logger.error(f"获取数据库连接失败: {e}")
        raise


# 执行 SQL 查询并返回结果
def execute_sql_query(sql_query):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        logger.info(f"执行 SQL 查询✔: {sql_query}")
        cursor.execute(sql_query)
        columns = cursor.column_names
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return {"columns": columns, "data": results}
    except mysql.connector.Error as err:
        logger.error(f"数据库错误: {err}")
        raise ValueError("数据库查询失败。")
