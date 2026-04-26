import json
import logging
from typing import Dict, Any, List

from app.common.llm_client import call_llm
from app.common.utils import convert_to_serializable

logger = logging.getLogger(__name__)


async def generate_natural_answer(
    user_question: str, query_result: List[Dict[str, Any]]
) -> str:
    """基于查询结果生成自然语言答案"""
    try:
        if not query_result:
            return "根据您的查询条件，没有找到相关数据。"

        result_summary = f"查询返回了 {len(query_result)} 条记录。"
        serializable_result = convert_to_serializable(query_result)

        sample_count = 3 if len(serializable_result) <= 5 else 2
        sample_data = json.dumps(
            serializable_result[:sample_count], ensure_ascii=False, indent=2
        )

        prompt = f"""
        用户问题: {user_question}
        
        查询结果摘要: {result_summary}
        样本数据: {sample_data}
        
        请基于查询结果，用自然语言回答用户的问题。
        
        **严格要求：**
        1. 语言简洁明了
        2. 突出关键数据
        3. 如果有多条记录，给出总体概况
        4. 用中文回答
        5. 只返回纯文本答案，不要任何格式化标记或解释前缀
        6. 不要返回JSON格式，只返回自然语言文本
        """

        answer = await call_llm([
            {
                "role": "system",
                "content": "你是一个数据分析助手，根据查询结果回答用户问题。只返回纯文本答案，不要任何格式化或JSON格式。",
            },
            {"role": "user", "content": prompt},
        ])

        return answer.strip()

    except Exception as e:
        logger.error(f"生成自然语言答案失败: {e}")
        return f"查询成功，共找到 {len(query_result)} 条相关记录。"
