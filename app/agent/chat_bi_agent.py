"""
Chat-BI 主要Agent协调器

这个模块负责协调所有的AI智能代理组件，提供统一的接口
包含：
- SQL生成代理
- 自然语言答案生成代理  
- 模板管理代理
- 查询解析代理
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
    """
    Chat-BI智能代理主类
    
    提供统一的接口来访问所有agent功能
    """
    
    @staticmethod
    async def generate_sql(user_question: str, schema_context: Optional[str] = None) -> str:
        """
        生成SQL查询
        
        Args:
            user_question: 用户问题
            schema_context: 可选的schema上下文，如果不提供则自动获取
            
        Returns:
            SQL查询语句
        """
        if schema_context:
            return await parse_query_to_sql(user_question, schema_context)
        else:
            return await generate_sql_with_context(user_question)
    
    @staticmethod
    async def generate_answer(user_question: str, query_result: List[Dict[str, Any]]) -> str:
        """
        基于查询结果生成自然语言答案
        
        Args:
            user_question: 用户问题
            query_result: 查询结果
            
        Returns:
            自然语言答案
        """
        return await generate_natural_answer(user_question, query_result)
    
    @staticmethod
    async def save_template(user_question: str, sql_query: str, user_embedding: List[float]):
        """
        保存SQL模板
        
        Args:
            user_question: 用户问题
            sql_query: SQL查询
            user_embedding: 用户问题的向量嵌入
        """
        await store_new_template(user_question, sql_query, user_embedding)
    
    @staticmethod
    async def create_template_description(user_question: str, sql_query: str) -> str:
        """
        为SQL模板生成描述
        
        Args:
            user_question: 用户问题
            sql_query: SQL查询
            
        Returns:
            模板描述
        """
        return await generate_template_description(user_question, sql_query)
    
    @staticmethod
    def extract_parameters(sql_query: str) -> List[str]:
        """
        从SQL中提取参数
        
        Args:
            sql_query: SQL查询
            
        Returns:
            参数列表
        """
        return extract_sql_parameters(sql_query)
    
    @staticmethod
    def clean_sql_response(response: str) -> str:
        """
        清理AI响应，提取纯SQL
        
        Args:
            response: AI响应
            
        Returns:
            清理后的SQL语句
        """
        return extract_sql_from_response(response)
    
    @staticmethod
    def build_database_schema_description(schema_info: Dict[str, Any]) -> str:
        """
        构建数据库Schema描述
        
        Args:
            schema_info: 数据库schema信息
            
        Returns:
            Schema文本描述
        """
        return build_schema_description(schema_info)


# 提供便捷的函数接口，保持向后兼容
async def process_user_query(
    user_question: str, 
    query_result: Optional[List[Dict[str, Any]]] = None,
    user_embedding: Optional[List[float]] = None
) -> Dict[str, Any]:
    """
    处理用户查询的完整流程
    
    Args:
        user_question: 用户问题
        query_result: 查询结果（如果已有）
        user_embedding: 用户问题向量（如果已有）
        
    Returns:
        包含SQL和答案的结果字典
    """
    try:
        result = {}
        
        # 1. 生成SQL
        sql_query = await ChatBIAgent.generate_sql(user_question)
        result['sql'] = sql_query
        
        # 2. 如果有查询结果，生成自然语言答案
        if query_result is not None:
            answer = await ChatBIAgent.generate_answer(user_question, query_result)
            result['answer'] = answer
            
            # 3. 保存模板（如果有向量嵌入）
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