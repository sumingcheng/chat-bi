from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

from app.common.llm_registry import (
    get_active_selection,
    list_models,
    list_providers,
    set_active_selection,
)
from app.server.models.response import success_response, error_response


llm = APIRouter()


class LLMSelectionRequest(BaseModel):
    provider: str = Field(..., description="LLM provider，例如 openai / deepseek")
    model: str = Field(..., description="模型 ID")


@llm.get("/llm/providers")
async def get_llm_providers():
    """获取已支持的 LLM 渠道，不返回任何密钥"""
    try:
        return success_response({
            "providers": list_providers(),
            "selection": get_active_selection(),
        })
    except Exception as e:
        return error_response(code=500, message=str(e))


@llm.get("/llm/models")
async def get_llm_models(provider: str = Query(..., description="LLM provider")):
    """根据 provider 实时拉取模型列表"""
    try:
        return success_response({
            "provider": provider,
            "models": await list_models(provider),
        })
    except Exception as e:
        return error_response(code=500, message=str(e))


@llm.get("/llm/selection")
async def get_llm_selection():
    """获取当前运行时生效的 LLM provider/model"""
    try:
        return success_response(get_active_selection())
    except Exception as e:
        return error_response(code=500, message=str(e))


@llm.post("/llm/selection")
async def update_llm_selection(request: LLMSelectionRequest):
    """切换当前运行时生效的 LLM provider/model"""
    try:
        return success_response(set_active_selection(request.provider, request.model))
    except Exception as e:
        return error_response(code=400, message=str(e))
