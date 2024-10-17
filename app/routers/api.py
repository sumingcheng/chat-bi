import os
from fastapi import APIRouter, HTTPException
from app.models.schemas import QueryRequest
from app.handlers.query_handler import process_query

router = APIRouter()


@router.post("/query")
def handle_query(request: QueryRequest):
    try:
        user_input = request.user_input

        # 调用处理函数
        result = process_query(user_input)
        return result

    except Exception as e:
        # 开发环境返回详细错误信息
        if os.getenv('ENVIRONMENT') == 'development':
            raise HTTPException(status_code=500, detail=str(e))
        else:
            raise HTTPException(status_code=500, detail="服务器内部错误，请稍后重试。")
