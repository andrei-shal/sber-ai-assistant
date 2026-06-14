import json

from services.llm import chat
import os

from dotenv import load_dotenv

load_dotenv()

with open(
    "prompts/control_assistant.txt",
    encoding="utf-8"
) as f:
    SYSTEM_PROMPT = f.read()

async def control_node(state):

    button = ""

    if state["button_correct"]:
        button = "корректная или не отправлена"
    else:
        button = "не корректная"

    user_prompt = f"""
Вопрос:
{state["question"]}

Кнопка: {button}

Ответ:
{state["answer"]}
"""

    print (button)

    history = state.get("messages", [])

    answer = await chat(os.getenv("ASSISTANT"), SYSTEM_PROMPT, user_prompt, history[-4:])

    print(answer)

    try:
        parsed = json.loads(answer)
    except (json.JSONDecodeError, KeyError, TypeError):
        return {
            "answer": "К сожалению, я не могу предоставить корректный ответ на данный вопрос или помочь с решением проблемы. Система работает в тестовом режиме, имеет доступ не ко всем данным и в отдельных случаях может работать некорректно. Рекомендуем обратиться в чат поддержки для получения помощи специалиста.",
            "support": "True",
            "messages": history[-20:]
        }

    messages = (history + [
        {
            "role": "user",
            "content": state["question"]
        },
        {
            "role": "assistant",
            "content": parsed.get("answer", "")
        }
    ])[-20:]

    return {
        "answer": parsed.get("answer", ""),
        "support": str(parsed.get("support", True)),
        "messages": messages
    }