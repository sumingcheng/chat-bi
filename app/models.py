from pydantic import BaseModel


# 定义请求体模型
class QueryRequest(BaseModel):
    user_input: str
