from fastapi import APIRouter, HTTPException
from database.mysql import get_system_db_connection
from journal.logging import logger

router = APIRouter()


@router.get("/history")
async def get_history(
    start_date: str = None, end_date: str = None, keyword: str = None
):
    """获取查询历史记录，支持按时间范围和关键词过滤"""
    try:
        conn = get_system_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM query_history WHERE 1=1"
        params = []

        if start_date:
            query += " AND created_at >= %s"
            params.append(start_date)
        if end_date:
            query += " AND created_at <= %s"
            params.append(end_date)
        if keyword:
            query += " AND user_input LIKE %s"
            params.append(f"%{keyword}%")

        cursor.execute(query, params)
        history = cursor.fetchall()
        cursor.close()
        conn.close()

        return history

    except Exception as e:
        logger.error(f"获取历史记录失败: {e}")
        raise HTTPException(status_code=500, detail="获取历史记录失败") 