from services.llm import chat
import os

from dotenv import load_dotenv

load_dotenv()

with open(
    "prompts/rag_assistant.txt",
    encoding="utf-8"
) as f:
    SYSTEM_PROMPT = f.read()

def rag_assistant_node(state):

    user_prompt = f"""
Документы найденные по теме вопроса:

{state["documents_context"]}

Вопрос:

{state["question"]}

Отвечай только по контексту.

Если ответа нет в контексте,
сообщи об этом явно.
"""

    history = state.get("messages", [])

    answer = chat(os.getenv("ASSISTANT"), SYSTEM_PROMPT, user_prompt, history[-4:])

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