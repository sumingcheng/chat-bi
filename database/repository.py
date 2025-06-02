import json
import logging
from typing import List, Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from .base import get_business_session, get_system_session

logger = logging.getLogger(__name__)
class BusinessRepository:
    """业务数据库访问层"""
    
    @staticmethod
    async def execute_query(sql: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        执行业务数据库查询
        """
        try:
            logger.debug(f"执行业务数据库查询: {sql}")
            if params:
                logger.debug(f"查询参数: {params}")
            
            async for session in get_business_session():
                result = await session.execute(text(sql), params or {})
                columns = result.keys()
                rows = result.fetchall()
                data = [dict(zip(columns, row)) for row in rows]
                
                logger.info(f"业务数据库查询完成，返回 {len(data)} 条记录")
                return data
                
        except Exception as e:
            logger.error(f"业务数据库查询失败: {e}")
            logger.error(f"执行的SQL: {sql}")
            if params:
                logger.error(f"查询参数: {params}")
            raise


class SystemRepository:
    """系统数据库访问层"""
    
    @staticmethod
    async def execute_query(sql: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        执行系统数据库查询
        """
        try:
            logger.debug(f"执行系统数据库查询: {sql}")
            if params:
                logger.debug(f"查询参数: {params}")
            
            async for session in get_system_session():
                result = await session.execute(text(sql), params or {})
                columns = result.keys()
                rows = result.fetchall()
                data = [dict(zip(columns, row)) for row in rows]
                
                logger.info(f"系统数据库查询完成，返回 {len(data)} 条记录")
                return data
                
        except Exception as e:
            logger.error(f"系统数据库查询失败: {e}")
            logger.error(f"执行的SQL: {sql}")
            if params:
                logger.error(f"查询参数: {params}")
            raise
    
    @staticmethod
    async def save_query_history(
        query_id: str,
        user_input: str,
        sql_query: str = None,
        result: Any = None,
        satisfaction_level: str = None,
        visualization_type: str = 'table'
    ):
        """
        保存查询历史
        """
        try:
            logger.debug(f"保存查询历史，查询ID: {query_id}")
            from .system_models import QueryHistory
            
            async for session in get_system_session():
                history = QueryHistory(
                    query_id=query_id,
                    user_input=user_input,
                    sql_query=sql_query,
                    result=json.dumps(result, ensure_ascii=False) if result else None,
                    satisfaction_level=satisfaction_level,
                    visualization_type=visualization_type
                )
                session.add(history)
                await session.commit()
                logger.info(f"查询历史保存成功，查询ID: {query_id}")
                return history
                
        except Exception as e:
            logger.error(f"保存查询历史失败: {e}")
            logger.error(f"查询ID: {query_id}")
            raise
    
    @staticmethod
    async def get_sql_templates(scenario: str = None) -> List[Dict[str, Any]]:
        """
        获取SQL模板
        """
        try:
            logger.debug(f"获取SQL模板，场景: {scenario or '全部'}")
            
            sql = """
            SELECT t.*, GROUP_CONCAT(
                CONCAT(p.param_name, ':', p.param_type, ':', IFNULL(p.param_description, ''))
                SEPARATOR '|'
            ) as params
            FROM sql_templates t
            LEFT JOIN sql_template_params p ON t.id = p.template_id
            """
            
            if scenario:
                sql += " WHERE t.scenario = :scenario"
                params = {"scenario": scenario}
            else:
                params = {}
                
            sql += " GROUP BY t.id ORDER BY t.created_at DESC"
            
            result = await SystemRepository.execute_query(sql, params)
            logger.info(f"获取到 {len(result)} 个SQL模板")
            return result
            
        except Exception as e:
            logger.error(f"获取SQL模板失败: {e}")
            raise 