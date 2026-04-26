import os
from openai import OpenAI
from src.config.env import settings

# 从环境变量中获取您的API KEY，配置方法见：https://www.volcengine.com/docs/82379/1399008
api_key = settings.ARK_API_KEY

client = OpenAI(
    base_url=settings.LLM_BASE_URL,
    api_key=api_key,
)

response = client.responses.create(
    model=settings.LLM_MODEL_NAME,
    input=[
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "你是谁"
                },
            ],
        }
    ]
)

print(response)