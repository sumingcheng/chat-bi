"""
Chat-BI 智能代理协调器

协调SQL生成、答案生成、模板管理等AI组件
"""

import logging
from typing import Dict, Any, List, Optional

from .sql_generator import (
    generate_sql_with_context,
    build_schema_description,
    extract_sql_from_response,
    extract_sql_parameters
)
from .answer_generator import generate_natural_answer
from .template_manager import (
    store_new_template,
    generate_template_description
)
from .parse_query_to_sql import parse_query_to_sql

logger = logging.getLogger(__name__)


class ChatBIAgent:
    """Chat-BI智能代理主类"""
    
    @staticmethod
    async def generate_sql(user_question: str, schema_context: Optional[str] = None) -> str:
        """生成SQL查询"""
        if schema_context:
            return await parse_query_to_sql(user_question, schema_context)
        else:
            return await generate_sql_with_context(user_question)
    
    @staticmethod
    async def generate_answer(user_question: str, query_result: List[Dict[str, Any]]) -> str:
        """基于查询结果生成自然语言答案"""
        return await generate_natural_answer(user_question, query_result)
    
    @staticmethod
    async def save_template(user_question: str, sql_query: str, user_embedding: List[float]):
        """保存SQL模板"""
        await store_new_template(user_question, sql_query, user_embedding)
    
    @staticmethod
    async def create_template_description(user_question: str, sql_query: str) -> str:
        """为SQL模板生成描述"""
        return await generate_template_description(user_question, sql_query)
    
    @staticmethod
    def extract_parameters(sql_query: str) -> List[str]:
        """从SQL中提取参数"""
        return extract_sql_parameters(sql_query)
    
    @staticmethod
    def clean_sql_response(response: str) -> str:
        """清理AI响应，提取纯SQL"""
        return extract_sql_from_response(response)
    
    @staticmethod
    def build_database_schema_description(schema_info: Dict[str, Any]) -> str:
        """构建数据库Schema描述"""
        return build_schema_description(schema_info)


async def process_user_query(
    user_question: str, 
    query_result: Optional[List[Dict[str, Any]]] = None,
    user_embedding: Optional[List[float]] = None
) -> Dict[str, Any]:
    """处理用户查询的完整流程"""
    try:
        result = {}
        
        sql_query = await ChatBIAgent.generate_sql(user_question)
        result['sql'] = sql_query
        
        if query_result is not None:
            answer = await ChatBIAgent.generate_answer(user_question, query_result)
            result['answer'] = answer
            
            if user_embedding is not None:
                await ChatBIAgent.save_template(user_question, sql_query, user_embedding)
        
        return {
            'success': True,
            'data': result
        }
        
    except Exception as e:
        logger.error(f"处理用户查询失败: {e}")
        return {
            'success': False,
            'error': str(e)
        } 