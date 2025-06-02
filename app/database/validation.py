import logging
import sqlparse
from sqlparse.tokens import Keyword, DML

logger = logging.getLogger(__name__)

DANGEROUS_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "CREATE",
    "ALTER",
    "TRUNCATE",
    "GRANT",
    "REVOKE",
    "EXEC",
    "EXECUTE",
    "CALL",
    "LOAD_FILE",
    "INTO OUTFILE",
    "INTO DUMPFILE",
}


def validate_sql_query(sql_query: str) -> bool:
    """验证SQL查询安全性"""
    logger.debug(f"开始验证SQL查询安全性: {sql_query[:100]}...")

    if not sql_query or not sql_query.strip():
        logger.warning("SQL查询为空")
        raise ValueError("SQL查询不能为空")

    try:
        parsed = sqlparse.parse(sql_query)
        logger.debug("SQL语法解析成功")
    except Exception as e:
        logger.error(f"SQL语法解析失败: {e}")
        raise ValueError(f"SQL语法错误: {e}")

    if not parsed:
        logger.error("无法解析SQL语句")
        raise ValueError("无法解析SQL语句")

    for statement in parsed:
        if statement.get_type() != "SELECT":
            logger.warning(f"发现非SELECT语句: {statement.get_type()}")
            raise ValueError("仅允许执行 SELECT 查询")

        if contains_dangerous_keywords(statement):
            logger.warning("SQL包含危险操作关键字")
            raise ValueError("SQL包含危险操作关键字")

    logger.info("SQL查询安全验证通过")
    return True


def is_select_statement(statement) -> bool:
    """检查是否为SELECT语句"""
    return statement.get_type() == "SELECT"


def contains_dangerous_keywords(statement) -> bool:
    """检查危险关键字"""
    tokens = list(statement.flatten())

    for token in tokens:
        if token.ttype is Keyword and token.value.upper() in DANGEROUS_KEYWORDS:
            logger.warning(f"发现危险关键字: {token.value}")
            return True
        if hasattr(token, "value") and isinstance(token.value, str):
            token_upper = token.value.upper()
            for keyword in DANGEROUS_KEYWORDS:
                if keyword in token_upper:
                    logger.warning(f"在字符串中发现危险关键字: {keyword}")
                    return True

    return False


def sanitize_sql_query(sql_query: str) -> str:
    """清理SQL查询"""
    logger.debug("开始清理SQL查询")

    if not sql_query:
        logger.debug("SQL查询为空，返回空字符串")
        return ""

    try:
        parsed = sqlparse.parse(sql_query)[0]
        formatted = sqlparse.format(
            str(parsed), strip_comments=True, strip_whitespace=True
        )
        logger.debug("SQL查询清理完成")
        return formatted.strip()
    except Exception as e:
        logger.warning(f"SQL解析失败，使用基础清理: {e}")
        cleaned = " ".join(sql_query.split())
        logger.debug("基础清理完成")
        return cleaned
