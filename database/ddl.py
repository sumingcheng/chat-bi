from mysql.connector import Error
import mysql.connector
import mysql
import json
import os
from datetime import datetime


class DDLGenerator:
    def __init__(self):
        self.config = self._get_config()
        self.connection = None

    def _get_config(self):
        """从环境变量获取数据库配置"""
        return {
            "host": os.environ.get("DB_HOST", "172.22.220.64"),
            "port": int(os.environ.get("DB_PORT", "33306")),
            "user": os.environ.get("DB_USER", "root"),
            "password": os.environ.get("DB_PASSWORD", "admin123456"),
            "database": os.environ.get("DB_NAME", "query_db"),
        }

    def connect(self):
        """连接数据库"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            print(f"成功连接到数据库 {self.config['database']}")
            return True
        except Error as e:
            print(f"连接数据库失败: {e}")
            return False

    def get_all_tables(self):
        """获取所有表名"""
        cursor = self.connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        cursor.close()
        return tables

    def get_table_ddl(self, table_name):
        """获取表的DDL"""
        cursor = self.connection.cursor()
        cursor.execute(f"SHOW CREATE TABLE {table_name}")
        ddl = cursor.fetchone()[1]
        cursor.close()
        return ddl

    def save_ddl_to_json(self, tables_ddl):
        """保存DDL到JSON文件"""
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_file = os.path.join(script_dir, "db_ddl.json")

        schema_data = {
            "timestamp": datetime.now().isoformat(),
            "database": self.config["database"],
            "tables": tables_ddl,
        }

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(schema_data, f, indent=2, ensure_ascii=False)

        print(f"DDL已保存到: {output_file}")
        return output_file

    def generate(self):
        """生成DDL的主流程"""
        if not self.connect():
            return False

        try:
            tables = self.get_all_tables()
            tables_ddl = {}

            for table in tables:
                ddl = self.get_table_ddl(table)
                tables_ddl[table] = ddl
                print(f"已获取表 {table} 的DDL")

            self.save_ddl_to_json(tables_ddl)
            return True

        except Error as e:
            print(f"生成DDL时出错: {e}")
            return False

        finally:
            if self.connection:
                self.connection.close()
                print("数据库连接已关闭")


def main():
    generator = DDLGenerator()
    generator.generate()


if __name__ == "__main__":
    main()
