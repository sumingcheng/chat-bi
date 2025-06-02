from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional
from app.server.service.query import query_db_sql
from app.server.models.response import success_response, error_response

query = APIRouter()


class ChatRequest(BaseModel):
    question: str = Field(..., description="用户的自然语言问题")
    session_id: Optional[str] = Field(None, description="可选的会话ID")


@query.post("/chat")
async def chat_query(request: ChatRequest):
    """Chat-BI 智能对话查询接口"""
    try:
        result = await query_db_sql(request.question, request.session_id)

        # 如果service层处理成功，返回成功响应
        if result.get("success", False):
            return success_response(result["data"])
        else:
            # 如果service层返回失败，使用错误响应
            error_info = result.get("error", {})
            return error_response(
                code=error_info.get("code", 500),
                message=error_info.get("message", "查询处理失败"),
            )

    except Exception as e:
        return error_response(code=500, message=f"系统异常: {str(e)}")


# 保留原来的接口作为兼容
@query.post("/query")
async def query_db():
    return success_response({"message": "请使用 /chat 接口进行查询"})
