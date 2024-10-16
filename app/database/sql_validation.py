import sqlparse


# 验证SQL查询，仅允许SELECT语句，避免SQL注入
# 建议使用预编译语句或参数化查询，从根本上防止 SQL 注入攻击
def validate_sql_query(sql_query):
    parsed = sqlparse.parse(sql_query)
    for statement in parsed:
        if statement.get_type() != 'SELECT':
            raise ValueError("仅允许执行 SELECT 查询。")
