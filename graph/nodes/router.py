from services.llm import chat
from services.pipeline_logger import get_logger
import os

from dotenv import load_dotenv

load_dotenv()

log = get_logger()

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
    route = await chat(os.getenv("SYSTEM_MODEL"), SYSTEM_PROMPT, user_prompt,history[-4:])

    log.info(f"RAW router response: {route}")

    route_text = str(route).strip()
    normalized = route_text.lower()
    if normalized not in {"rag", "navigation", "user_data"}:
        log.warn(f"Неизвестный маршрут '{route_text}', fallback → rag")
        normalized = "rag"

    log.route(normalized)

    return {
        "route": normalized
    }
