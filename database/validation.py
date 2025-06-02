import sqlparse
from sqlparse.tokens import Keyword, DML


DANGEROUS_KEYWORDS = {
    'INSERT', 'UPDATE', 'DELETE', 'DROP', 'CREATE', 'ALTER', 
    'TRUNCATE', 'GRANT', 'REVOKE', 'EXEC', 'EXECUTE',
    'CALL', 'LOAD_FILE', 'INTO OUTFILE', 'INTO DUMPFILE'
}


def validate_sql_query(sql_query: str) -> bool:
    """验证SQL查询安全性"""
    if not sql_query or not sql_query.strip():
        raise ValueError("SQL查询不能为空")
    
    # 解析SQL语句
    try:
        parsed = sqlparse.parse(sql_query)
    except Exception as e:
        raise ValueError(f"SQL语法错误: {e}")
    
    if not parsed:
        raise ValueError("无法解析SQL语句")
    
    # 检查每个语句
    for statement in parsed:
        if statement.get_type() != "SELECT":
            raise ValueError("仅允许执行 SELECT 查询")
        
        if contains_dangerous_keywords(statement):
            raise ValueError("SQL包含危险操作关键字")
    
    return True


def is_select_statement(statement) -> bool:
    """检查是否为SELECT语句"""
    return statement.get_type() == "SELECT"


def contains_dangerous_keywords(statement) -> bool:
    """检查危险关键字"""
    tokens = list(statement.flatten())
    
    for token in tokens:
        if token.ttype is Keyword and token.value.upper() in DANGEROUS_KEYWORDS:
            return True
        # 检查字符串中是否包含危险操作
        if hasattr(token, 'value') and isinstance(token.value, str):
            token_upper = token.value.upper()
            for keyword in DANGEROUS_KEYWORDS:
                if keyword in token_upper:
                    return True
    
    return False


def sanitize_sql_query(sql_query: str) -> str:
    """清理SQL查询"""
    if not sql_query:
        return ""
    
    # 解析并格式化SQL
    try:
        parsed = sqlparse.parse(sql_query)[0]
        # 移除注释
        formatted = sqlparse.format(
            str(parsed), 
            strip_comments=True, 
            strip_whitespace=True
        )
        return formatted.strip()
    except:
        # 如果解析失败，返回清理后的原始查询
        return ' '.join(sql_query.split()) 