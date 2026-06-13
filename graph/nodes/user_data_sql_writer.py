from services.llm import chat
import os

from dotenv import load_dotenv

load_dotenv()

with open(
    "prompts/user_data_sql_writer.txt",
    encoding="utf-8"
) as f:
    SYSTEM_PROMPT = f.read()

async def user_data_sql_writer_node(state):

    user_prompt = f"""
Вопрос:

{state["question"]}
"""

    history = state.get("messages", [])

    answer = await chat(os.getenv("SYSTEM_MODEL"), SYSTEM_PROMPT, user_prompt, history[-4:])

    return {
        "user_sql": answer
    }