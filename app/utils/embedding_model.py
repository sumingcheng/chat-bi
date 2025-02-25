import openai

from config.main import Config

# 设置 OpenAI API 密钥
openai.api_key = Config.OPENAI_API_KEY


def get_text_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    embedding = response['data'][0]['embedding']
    return embedding
    