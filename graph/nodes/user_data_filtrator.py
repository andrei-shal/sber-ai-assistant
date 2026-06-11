from services.llm import chat
import os

from dotenv import load_dotenv

load_dotenv()

with open(
    "prompts/user_data_filtrator.txt",
    encoding="utf-8"
) as f:
    SYSTEM_PROMPT = f.read()

async def user_data_filtrator_node(state):

    user_prompt = f"""
Платежи:
{state["user_context"]}

Вопрос:

{state["question"]}

Отвечай только по контексту.

Если ответа нет в контексте,
сообщи об этом явно.
"""

    history = state.get("messages", [])

    answer = await chat(os.getenv("SYSTEM_MODEL"), SYSTEM_PROMPT, user_prompt, history[-4:])

    return {
        "filtered_user_context": answer
    }