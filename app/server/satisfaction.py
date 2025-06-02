from fastapi import APIRouter, HTTPException
from app.models.schemas import SatisfactionRequest
from database.mysql import get_system_db_connection
from journal.logging import logger

router = APIRouter()


@router.post("/satisfaction")
async def record_satisfaction(request: SatisfactionRequest):
    """记录用户对查询结果的满意度评价"""
    try:
        conn = get_system_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE query_history SET satisfaction_level = %s WHERE query_id = %s",
            (request.satisfaction_level, request.query_id),
        )
        conn.commit()
        cursor.close()
        conn.close()

        # 如果用户满意，保存到向量库
        if request.satisfaction_level == "satisfied":
            # 获取查询记录
            conn = get_system_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(
                "SELECT user_input, sql_query FROM query_history WHERE query_id = %s",
                (request.query_id,),
            )
            record = cursor.fetchone()
            cursor.close()
            conn.close()

            if record:
                from utils.milvus import (
                    connect_milvus,
                    get_or_create_collection,
                    insert_data,
                )

                connect_milvus()
                collection = get_or_create_collection()
                insert_data(collection, [record["user_input"]], [record["sql_query"]])

        return {"message": "评价记录成功"}

    except Exception as e:
        logger.error(f"记录满意度失败: {e}")
        raise HTTPException(status_code=500, detail="记录满意度失败") 