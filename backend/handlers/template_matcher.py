from database.mysql import get_business_db_connection
from journal.logging import logger
from utils.openai import client as openai_client
from typing import Optional, Tuple, List, Dict
import json


def get_template_parameters(template_text: str) -> List[str]:
    """
    从SQL模板中提取参数名
    """
    import re

    # 匹配 {parameter} 形式的参数
    params = re.findall(r"\{(\w+)\}", template_text)
    return list(set(params))


def match_sql_template(user_input: str) -> Optional[Tuple[str, dict]]:
    """
    尝试将用户输入与SQL模板匹配
    返回: (SQL模板, 参数字典) 或 None
    """
    try:
        conn = get_business_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 获取所有模板及其参数
        cursor.execute(
            """
            SELECT t.*, GROUP_CONCAT(p.param_name) as params
            FROM sql_templates t
            LEFT JOIN sql_template_params p ON t.id = p.template_id
            GROUP BY t.id
        """
        )
        templates = cursor.fetchall()
        cursor.close()
        conn.close()

        if not templates:
            return None

        # 构建提示词
        prompt = f"""
        用户问题: {user_input}

        可用的SQL模板:
        """
        for t in templates:
            prompt += f"\n模板ID: {t['id']}\n描述: {t['description']}\n场景: {t['scenario']}\n"
            if t["params"]:
                prompt += f"参数: {t['params']}\n"
            prompt += f"SQL: {t['sql_text']}\n"

        prompt += "\n请判断用户问题是否匹配以上任一模板。如果匹配，请提取参数值。"
        prompt += "\n返回格式: JSON {'matched': true/false, 'template_id': int, 'parameters': {参数名:参数值}}"

        # 调用OpenAI进行模板匹配和参数提取
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "你是一个SQL模板匹配专家"},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        # 解析响应
        result = json.loads(response.choices[0].message.content)

        if result.get("matched"):
            # 获取匹配的模板
            template = next(t for t in templates if t["id"] == result["template_id"])
            return template["sql_text"], result["parameters"]

        return None

    except Exception as e:
        logger.error(f"模板匹配失败: {e}")
        return None
