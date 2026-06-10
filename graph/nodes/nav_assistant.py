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


def nav_assistant_node(state):

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

    response = chat(
        os.getenv("ASSISTANT"),
        SYSTEM_PROMPT,
        user_prompt,
        history[-4:]
    )

    parsed = json.loads(response)

    messages = (
        history
        + [
            {
                "role": "user",
                "content": state["question"]
            },
            {
                "role": "assistant",
                "content": parsed["answer"]
            }
        ]
    )[-20:]

    return {
        "answer": parsed["answer"],
        "button": parsed["button"],
        "messages": messages
    }