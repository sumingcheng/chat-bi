from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Dict, Any

T = TypeVar("T")


# 错误模型
class ErrorDetail(BaseModel):
    code: int
    message: str


# 通用响应模型
class ResponseModel(BaseModel, Generic[T]):
    data: T
    success: bool
    error: Dict[str, Any] = Field(default_factory=dict)


def success_response(data: Any) -> ResponseModel:
    """创建成功响应"""
    return ResponseModel(data=data, success=True)


def error_response(code: int, message: str) -> ResponseModel:
    """创建错误响应"""
    return ResponseModel(
        data={}, success=False, error={"code": code, "message": message}
    )
