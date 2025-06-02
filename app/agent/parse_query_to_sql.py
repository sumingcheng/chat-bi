import logging
from app.common import openai_clinet

logger = logging.getLogger(__name__)


async def parse_query_to_sql(user_prompt: str) -> str:
    try:
        response = await openai_clinet.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "你是一个SQL查询专家，请将用户的自然语言问题转换为SQL查询语句。仅返回SQL查询语句，不要返回任何解释或说明。",
                },
                {"role": "user", "content": user_prompt},
            ],
            temperature=0,
            response_format={"type": "json_object"},
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"OpenAI API调用失败: {e}")
        raise


user_prompt = "请查询所有用户"
