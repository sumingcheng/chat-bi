from mysql.connector import Error
import mysql.connector
import mysql
import json
import os
from datetime import datetime


def get_db_connection():
    try:
        # 从环境变量获取数据库配置，如果不存在则使用默认值
        host = os.environ.get('DB_HOST', '127.0.0.1')
        port = int(os.environ.get('DB_PORT', '13306'))
        user = os.environ.get('DB_USER', 'root')
        password = os.environ.get('DB_PASSWORD', 'admin123456')
        database = os.environ.get('DB_NAME', 'chat_bi')

        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
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


# 将DDL保存为JSON格式
def save_ddl_to_json(tables_ddl, output_file=None):
    if output_file is None:
        # 使用当前时间创建文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"database_schema_{timestamp}.json"

    # 确保路径是相对于当前目录
    output_path = os.path.join(os.getcwd(), output_file)

    # 创建包含DDL和元数据的字典
    schema_data = {
        "timestamp": datetime.now().isoformat(),
        "database": os.environ.get('DB_NAME', 'chat_bi'),
        "tables": {}
    }

    for table_name, ddl in tables_ddl.items():
        schema_data["tables"][table_name] = {
            "ddl": ddl
        }

    # 写入JSON文件
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(schema_data, f, indent=2, ensure_ascii=False)

    print(f"DDL已保存到JSON文件: {output_path}")
    return output_path


# 主函数
def main():
    connection = None
    try:
        connection = get_db_connection()
        tables = get_all_tables(connection)
        tables_ddl = {}

        for table in tables:
            ddl = get_table_ddl(connection, table)
            tables_ddl[table] = ddl
            print(f"获取 {table} 的 DDL 成功")

        # 保存到JSON文件
        json_file = save_ddl_to_json(tables_ddl)

    except Error as e:
        print("连接 MySQL 时出错", e)
    finally:
        if connection:
            connection.close()


if __name__ == "__main__":
    main()
