from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.schemas import QueryRequest, QueryResponse
from handlers.query_handler import process_query
from journal.logging import logger
from database.connection import get_system_db
from handlers.template_matcher import match_sql_template
from utils.openai import parse_query_to_sql
from database.sql_validation import validate_sql_query

router = APIRouter()


@router.post("/query", response_model=QueryResponse)
async def handle_query(
    request: QueryRequest, db: AsyncSession = Depends(get_system_db)
):
    """处理用户查询请求"""
    try:
        result = await process_query(request.user_input, db)
        return QueryResponse(
            query_id=result["query_id"],
            data=result["data"],
            suggested_visualization=result["visualization_type"],
            sql_query=result["sql_query"],
            status="success",
        )
    except Exception as e:
        logger.error(f"处理查询失败: {e}")
        raise HTTPException(status_code=500, detail="查询处理失败")


@router.post("/preview-sql")
async def preview_sql(request: QueryRequest):
    """预览生成的SQL语句，不执行查询"""
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