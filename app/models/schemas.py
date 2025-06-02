from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from enum import Enum

class SatisfactionLevel(str, Enum):
    SATISFIED = "satisfied"
    NEUTRAL = "neutral"
    UNSATISFIED = "unsatisfied"

# 定义请求体模型
class QueryRequest(BaseModel):
    user_input: str

class QueryResponse(BaseModel):
    query_id: str
    data: List[Dict[str, Any]]
    suggested_visualization: str
    sql_query: Optional[str] = None
    status: str

class SatisfactionRequest(BaseModel):
    query_id: str
    satisfaction_level: SatisfactionLevel

class SQLTemplate(BaseModel):
    id: Optional[int] = None
    description: str
    sql_text: str
    scenario: str
    
class SQLTemplateCreate(BaseModel):
    description: str
    sql_text: str
    scenario: str

class SQLTemplateUpdate(BaseModel):
    description: Optional[str] = None
    sql_text: Optional[str] = None
    scenario: Optional[str] = None
