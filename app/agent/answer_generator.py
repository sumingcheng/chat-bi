import json
import logging
from typing import Dict, Any, List
from app.common.openai_clinet import call_openai_api

logger = logging.getLogger(__name__)


async def generate_natural_answer(
    user_question: str, query_result: List[Dict[str, Any]]
) -> str:
    """
    基于查询结果生成自然语言答案
    """
    try:
        if not query_result:
            return "根据您的查询条件，没有找到相关数据。"

        # 构建结果摘要
        result_summary = f"查询返回了 {len(query_result)} 条记录。"

        # 如果结果较少，可以具体描述
        if len(query_result) <= 5:
            sample_data = json.dumps(query_result[:3], ensure_ascii=False, indent=2)
        else:
            sample_data = json.dumps(query_result[:2], ensure_ascii=False, indent=2)

        prompt = f"""
        用户问题: {user_question}
        
        查询结果摘要: {result_summary}
        样本数据: {sample_data}
        
        请基于查询结果，用自然语言回答用户的问题。要求:
        1. 语言简洁明了
        2. 突出关键数据
        3. 如果有多条记录，给出总体概况
        4. 用中文回答
        """

        answer = await call_openai_api(
            [
                {
                    "role": "system",
                    "content": "你是一个数据分析助手，根据查询结果回答用户问题。",
                },
                {"role": "user", "content": prompt},
            ]
        )

        return answer

    except Exception as e:
        logger.error(f"生成自然语言答案失败: {e}")
        return f"查询成功，共找到 {len(query_result)} 条相关记录。" 