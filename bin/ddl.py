from mysql.connector import Error
import mysql.connector
import mysql
from config.main import Config


def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=Config.DB_HOST,
            port=int(Config.DB_PORT),
            user=Config.DB_USER,
            password=Config.DB_PASSWORD,
            database=Config.DB_NAME
        )
        print("Database connection successful")
        return connection
    except Error as e:
        print("Error connecting to MySQL:", e)
        return None


# 获取数据库中所有表的名称
def get_all_tables(connection):
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    cursor.close()
    return tables


# 获取单个表的DDL
def get_table_ddl(connection, table_name):
    cursor = connection.cursor()
    cursor.execute(f"SHOW CREATE TABLE {table_name}")
    create_table_stmt = cursor.fetchone()[1]  # 获取DDL语句
    cursor.close()
    return create_table_stmt


# 主函数
def main():
    connection = None
    try:
        connection = get_db_connection()
        tables = get_all_tables(connection)
        for table in tables:
            ddl = get_table_ddl(connection, table)
            print(f"DDL for {table}:\n{ddl}\n")
    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    main()
