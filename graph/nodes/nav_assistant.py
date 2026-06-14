import json

from services.llm import chat
import os

from dotenv import load_dotenv

load_dotenv()

with open(
    "prompts/nav_assistant.txt",
    encoding="utf-8"
) as f:
    SYSTEM_PROMPT = f.read()


async def nav_assistant_node(state):

    user_prompt = f"""
Найденные кандидаты для навигации:

{state["navigation_candidates_context"]}

Запрос пользователя:

{state["question"]}

Выбери наиболее подходящий маршрут.

Если подходящего маршрута нет,
сообщи об этом.

Верни результат согласно инструкции.
"""

    history = state.get("messages", [])

    response = await chat(
        os.getenv("ASSISTANT"),
        SYSTEM_PROMPT,
        user_prompt,
        history[-4:]
    )

    try:
        parsed = json.loads(response)
    except (json.JSONDecodeError, KeyError, TypeError):
        return {
            "answer": "Не удалось обработать ответ. Пожалуйста, уточните ваш вопрос.",
            "button": "",
        }

    return {
        "answer": parsed.get("answer", ""),
        "button": parsed.get("button") or "",
    }