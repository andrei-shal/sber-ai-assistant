from services.llm import chat
import os

from dotenv import load_dotenv

load_dotenv()

with open(
    "prompts/user_assistant.txt",
    encoding="utf-8"
) as f:
    SYSTEM_PROMPT = f.read()

async def user_assistant_node(state):
    print("gg")
    print(state["merged_context"])
    user_prompt = f"""
{state["merged_context"]}

Вопрос:

{state["question"]}

Отвечай только по контексту.

Если ответа нет в контексте,
сообщи об этом явно.
"""

    history = state.get("messages", [])

    answer = await chat(os.getenv("ASSISTANT"), SYSTEM_PROMPT, user_prompt, history[-4:])

    messages = (history + [
        {
            "role": "user",
            "content": state["question"]
        },
        {
            "role": "assistant",
            "content": answer
        }
    ])[-20:]

    return {
        "answer": answer,
        "button": "",
        "messages": messages
    }