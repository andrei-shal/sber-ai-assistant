from services.llm import chat
import os

from dotenv import load_dotenv

load_dotenv()

with open(
    "prompts/user_rag_req_writer.txt",
    encoding="utf-8"
) as f:
    SYSTEM_PROMPT = f.read()

async def user_rag_req_writer_node(state):
    user_prompt = f"""
Вопрос:

{state["question"]}
"""

    history = state.get("messages", [])
    search_query = await chat(os.getenv("SYSTEM_MODEL"), SYSTEM_PROMPT, user_prompt,history[-8:])

    print(search_query)

    return {
        "search_query": search_query
    }