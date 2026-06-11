from services.llm import chat
import os

from dotenv import load_dotenv

load_dotenv()

with open(
    "prompts/router.txt",
    encoding="utf-8"
) as f:
    SYSTEM_PROMPT = f.read()

async def router_node(state):
    user_prompt = f"""
Вопрос:

{state["question"]}
"""

    history = state.get("messages", [])
    route = await chat(os.getenv("SYSTEM_MODEL"), SYSTEM_PROMPT, user_prompt,history[-8:])

    print(route)

    return {
        "route": route.strip()
    }