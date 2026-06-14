from services.llm import chat
from services.pipeline_logger import get_logger
import os

from dotenv import load_dotenv

load_dotenv()

log = get_logger()

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

    log.info(f"Кнопка: {button}")

    user_prompt = f"""
Вопрос:
{state["question"]}

Кнопка: {button}

Ответ:
{state["answer"]}
"""

    history = state.get("messages", [])

    answer = await chat(os.getenv("ASSISTANT"), SYSTEM_PROMPT, user_prompt, history[-4:])

    log.info(f"RAW control ответ: {answer[:200]}")

    try:
        parsed = json.loads(answer)
    except (json.JSONDecodeError, KeyError, TypeError):
        log.error(f"Не удалось распарсить JSON: {answer[:300]}")
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