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

    parsed = json.loads(answer)

    messages = (history + [
        {
            "role": "user",
            "content": state["question"]
        },
        {
            "role": "assistant",
            "content": parsed["answer"]
        }
    ])[-20:]

    return {
        "answer": parsed["answer"],
        "support": str(parsed["support"]),
        "messages": messages
    }