import mysql.connector
from mysql.connector import pooling
from backend.config.main import Config
from backend.journal.logging import logger

# 业务数据库连接池配置
BUSINESS_DB_CONFIG = {
    "pool_name": "business_pool",
    "pool_size": 5,
    "host": Config.MYSQL_HOST,
    "user": Config.MYSQL_USER,
    "password": Config.MYSQL_PASSWORD,
    "database": "chat_bi"
}

# 系统数据库连接池配置
SYSTEM_DB_CONFIG = {
    "pool_name": "system_pool",
    "pool_size": 5,
    "host": Config.MYSQL_HOST,
    "user": Config.MYSQL_USER,
    "password": Config.MYSQL_PASSWORD,
    "database": "chat_bi_sys"
}

# 创建连接池
business_pool = mysql.connector.pooling.MySQLConnectionPool(**BUSINESS_DB_CONFIG)
system_pool = mysql.connector.pooling.MySQLConnectionPool(**SYSTEM_DB_CONFIG)

def get_business_db_connection():
    """
    获取业务数据库连接
    """
    try:
        return business_pool.get_connection()
    except Exception as e:
        logger.error(f"获取业务数据库连接失败: {e}")
        raise

def get_system_db_connection():
    """
    获取系统数据库连接
    """
    try:
        return system_pool.get_connection()
    except Exception as e:
        logger.error(f"获取系统数据库连接失败: {e}")
        raise

def execute_query(sql: str, params: tuple = None, is_system_db: bool = False):
    """
    执行查询
    """
    conn = get_system_db_connection() if is_system_db else get_business_db_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params)
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        logger.error(f"执行查询失败: {e}")
        raise
    finally:
        conn.close()
