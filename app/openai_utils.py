import os
from .logging_config import logger
import re
import openai
from openai import OpenAIError


# 将用户查询解析为SQL查询
def parse_query_to_sql(user_query):
    openai.api_key = os.getenv('OPENAI_API_KEY')

    if not openai.api_key:
        raise ValueError("未找到 OpenAI API 密钥，请设置 OPENAI_API_KEY 环境变量。")

    # 提供数据库结构信息
    database_schema = """
    数据库包含以下表：

    表名：products
    字段：
      - id (INT, PRIMARY KEY)
      - name (VARCHAR(255))

    表名：sales
    字段：
      - id (INT, PRIMARY KEY)
      - product_id (INT)
      - amount (DECIMAL(10,2))
      - date (DATE)
    """

    messages = [
        {"role": "system",
         "content": f"你是一个将自然语言查询直接转换为针对 MySQL 数据库的 SQL 查询的助手。请只返回 SQL 查询，不要添加任何额外的说明、解释或文本。\n\n数据库结构：\n{database_schema}"},
        {"role": "user", "content": f"请将以下自然语言查询直接转换为 SQL 查询，只返回 SQL 语句：\n\n\"{user_query}\""}
    ]

    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',  # 或 'gpt-4'，如果有权限
            messages=messages,
            temperature=0,
            max_tokens=150,
            n=1,
            stop=None
        )
        raw_response = response['choices'][0]['message']['content'].strip()
        logger.info(f"原始 OpenAI 响应: {raw_response}")

        # 提取纯粹的 SQL 查询
        sql_query = raw_response

        # 如果包含代码块，提取其中的内容
        if "```" in raw_response:
            matches = re.findall(r"```(?:sql)?\s*(.*?)\s*```", raw_response, re.DOTALL)
            if matches:
                sql_query = matches[0].strip()
        else:
            # 寻找第一个以 SELECT 开头的语句
            select_index = raw_response.lower().find("select")
            if select_index != -1:
                sql_query = raw_response[select_index:].strip()

        logger.info(f"提取的 SQL 查询: {sql_query}")
        return sql_query
    except OpenAIError as e:
        logger.error(f"OpenAI API 错误: {e}")
        raise ValueError("解析查询失败，请稍后重试。")
