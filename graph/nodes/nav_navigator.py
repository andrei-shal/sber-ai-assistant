from services.llm import chat
import os

from dotenv import load_dotenv

load_dotenv()

with open(
    "prompts/nav_navigator.txt",
    encoding="utf-8"
) as f:
    SYSTEM_PROMPT = f.read()

def nav_navigator_node(state):

    user_prompt = f"""
Вопрос:

{state["question"]}
"""

    history = state.get("messages", [])

    search_query = chat(os.getenv("SYSTEM_MODEL"), SYSTEM_PROMPT, user_prompt, history[-4:])

    return {
        "nav_search_query": search_query,
    }