import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL")
)

async def chat(model:str, system_prompt: str, user_prompt: str, history: list):
    response = await client.chat.completions.create(
        max_tokens = 10000,
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            *(history[-2:]),
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    return response.choices[0].message.content