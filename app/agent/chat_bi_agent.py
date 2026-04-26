"""Chat-BI 智能代理 — 协调 SQL 生成、答案生成、模板管理"""

import logging
from typing import Dict, Any, List, Optional

from .sql_generator import generate_sql_with_context, build_schema_description
from .answer_generator import generate_natural_answer
from .template_manager import store_new_template, generate_template_description
from .parse_query_to_sql import parse_query_to_sql
from app.common.utils import extract_sql_from_response, extract_sql_parameters

logger = logging.getLogger(__name__)


class ChatBIAgent:

    @staticmethod
    async def generate_sql(user_question: str, schema_context: Optional[str] = None) -> str:
        if schema_context:
            return await parse_query_to_sql(user_question, schema_context)
        return await generate_sql_with_context(user_question)

    @staticmethod
    async def generate_answer(user_question: str, query_result: List[Dict[str, Any]]) -> str:
        return await generate_natural_answer(user_question, query_result)

    @staticmethod
    async def save_template(user_question: str, sql_query: str, user_embedding: List[float]):
        await store_new_template(user_question, sql_query, user_embedding)

    @staticmethod
    async def create_template_description(user_question: str, sql_query: str) -> str:
        return await generate_template_description(user_question, sql_query)

    @staticmethod
    def extract_parameters(sql_query: str) -> List[str]:
        return extract_sql_parameters(sql_query)

    @staticmethod
    def clean_sql_response(response: str) -> str:
        return extract_sql_from_response(response)

    @staticmethod
    def build_database_schema_description(schema_info: Dict[str, Any]) -> str:
        return build_schema_description(schema_info)
