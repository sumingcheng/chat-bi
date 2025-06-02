import json
import logging
from typing import List, Dict, Any
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from .base import get_business_session, get_system_session, get_business_models

logger = logging.getLogger(__name__)


class BusinessRepository:
    """业务数据库访问层"""

    @staticmethod
    async def execute_query(
        sql: str, params: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """执行业务数据库查询"""
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

    @staticmethod
    async def get_database_schema() -> Dict[str, Any]:
        """获取业务数据库Schema"""
        try:
            logger.info("开始获取数据库Schema信息")

            schema_info = {"tables": [], "relationships": []}

            for model in get_business_models():
                table_info = await BusinessRepository._get_table_info(
                    model.__tablename__
                )
                schema_info["tables"].append(table_info)

            relationships = await BusinessRepository._get_foreign_keys()
            schema_info["relationships"] = relationships

            logger.info(f"Schema信息获取完成，包含 {len(schema_info['tables'])} 个表")
            return schema_info

        except Exception as e:
            logger.error(f"获取数据库Schema失败: {e}")
            raise

    @staticmethod
    async def _get_table_info(table_name: str) -> Dict[str, Any]:
        """获取表详细信息"""
        column_sql = """
        SELECT 
            COLUMN_NAME as column_name,
            DATA_TYPE as data_type,
            IS_NULLABLE as is_nullable,
            COLUMN_DEFAULT as column_default,
            COLUMN_KEY as column_key,
            EXTRA as extra,
            COLUMN_COMMENT as column_comment
        FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :table_name
        ORDER BY ORDINAL_POSITION
        """

        columns = await BusinessRepository.execute_query(
            column_sql, {"table_name": table_name}
        )

        table_comment_sql = """
        SELECT TABLE_COMMENT as table_comment
        FROM information_schema.TABLES 
        WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = :table_name
        """

        table_comment_result = await BusinessRepository.execute_query(
            table_comment_sql, {"table_name": table_name}
        )
        table_comment = (
            table_comment_result[0]["table_comment"] if table_comment_result else ""
        )

        return {
            "table_name": table_name,
            "table_comment": table_comment,
            "columns": columns,
        }

    @staticmethod
    async def _get_foreign_keys() -> List[Dict[str, Any]]:
        """获取外键关系"""
        fk_sql = """
        SELECT 
            TABLE_NAME as table_name,
            COLUMN_NAME as column_name,
            REFERENCED_TABLE_NAME as referenced_table_name,
            REFERENCED_COLUMN_NAME as referenced_column_name,
            CONSTRAINT_NAME as constraint_name
        FROM information_schema.KEY_COLUMN_USAGE 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND REFERENCED_TABLE_NAME IS NOT NULL
        ORDER BY TABLE_NAME, COLUMN_NAME
        """

        return await BusinessRepository.execute_query(fk_sql)

    @staticmethod
    async def get_table_ddl(table_name: str) -> str:
        """获取表DDL语句"""
        try:
            logger.debug(f"获取表 {table_name} 的DDL")

            ddl_sql = f"SHOW CREATE TABLE `{table_name}`"
            result = await BusinessRepository.execute_query(ddl_sql)

            if result:
                ddl = result[0].get("Create Table", "")
                logger.info(f"成功获取表 {table_name} 的DDL")
                return ddl
            else:
                raise ValueError(f"无法获取表 {table_name} 的DDL")

        except Exception as e:
            logger.error(f"获取表 {table_name} DDL失败: {e}")
            raise

    @staticmethod
    async def get_all_tables_ddl() -> Dict[str, str]:
        """获取所有业务表DDL"""
        try:
            logger.info("开始获取所有表的DDL")

            ddl_dict = {}
            for model in get_business_models():
                table_name = model.__tablename__
                ddl = await BusinessRepository.get_table_ddl(table_name)
                ddl_dict[table_name] = ddl

            logger.info(f"成功获取 {len(ddl_dict)} 个表的DDL")
            return ddl_dict

        except Exception as e:
            logger.error(f"获取所有表DDL失败: {e}")
            raise


class SystemRepository:
    """系统数据库访问层"""

    @staticmethod
    async def execute_query(
        sql: str, params: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """执行系统数据库查询"""
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
        visualization_type: str = "table",
    ):
        """保存查询历史"""
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
                    visualization_type=visualization_type,
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
        """获取SQL模板"""
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
