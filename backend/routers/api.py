import os
import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.schemas import QueryRequest, QueryResponse, SatisfactionRequest
from backend.handlers.query_handler import process_query
from backend.journal.logging import logger
from backend.database.connection import get_system_db
from backend.handlers.template_matcher import match_sql_template
from backend.utils.openai import parse_query_to_sql
from backend.database.sql_validation import validate_sql_query

router = APIRouter(prefix="/api")


@router.post("/query", response_model=QueryResponse)
async def handle_query(
    request: QueryRequest,
    db: AsyncSession = Depends(get_system_db)
):
    try:
        result = await process_query(request.user_input, db)
        return QueryResponse(
            query_id=result["query_id"],
            data=result["data"],
            suggested_visualization=result["visualization_type"],
            sql_query=result["sql_query"],
            status="success"
        )
    except Exception as e:
        logger.error(f"处理查询失败: {e}")
        raise HTTPException(status_code=500, detail="查询处理失败")


@router.post("/satisfaction")
async def record_satisfaction(request: SatisfactionRequest):
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
                from backend.utils.milvus import (
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


@router.get("/history")
async def get_history(
    start_date: str = None, end_date: str = None, keyword: str = None
):
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


@router.post("/preview-sql")
async def preview_sql(request: QueryRequest):
    try:
        # 尝试生成SQL但不执行
        sql_query = None

        # 1. 尝试模板匹配
        template_result = match_sql_template(request.user_input)
        if template_result:
            template_sql, params = template_result
            sql_query = template_sql.format(**params)

        # 2. 如果模板没匹配上，使用OpenAI生成SQL
        if not sql_query:
            sql_query = parse_query_to_sql(request.user_input)

        # 验证SQL安全性
        validate_sql_query(sql_query)

        return {"sql_query": sql_query}

    except Exception as e:
        logger.error(f"SQL预览失败: {e}")
        raise HTTPException(status_code=500, detail="SQL预览失败")
