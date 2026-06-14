from services.llm import chat
from services.pipeline_logger import get_logger
import os

from dotenv import load_dotenv

load_dotenv()

log = get_logger()

with open(
    "prompts/user_rag_req_writer.txt",
    encoding="utf-8"
) as f:
    SYSTEM_PROMPT = f.read()

async def user_rag_req_writer_node(state):
    user_prompt = f"""
Платежи:
{state["user_context"]}

Вопрос:

{state["question"]}
"""

    history = state.get("messages", [])
    search_query = await chat(os.getenv("SYSTEM_MODEL"), SYSTEM_PROMPT, user_prompt,history[-8:])

    log.info(f"User data -> RAG запрос: {search_query[:300]}")

    return {
        "search_query": search_query
    }