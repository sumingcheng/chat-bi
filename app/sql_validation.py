import sqlparse


# 验证SQL查询，仅允许SELECT语句，避免SQL注入
def validate_sql_query(sql_query):
    parsed = sqlparse.parse(sql_query)
    for statement in parsed:
        if statement.get_type() != 'SELECT':
            raise ValueError("仅允许执行 SELECT 查询。")
