from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

import uuid
import time

from services.pipeline_logger import get_logger

log = get_logger()

_session = {}

# Граф инициализируется один раз в lifespan
_graph = None


class QuestionRequest(BaseModel):
    data: str
    session_id: str | None = None


class QuestionResponse(BaseModel):
    answer: str
    button: str
    support: str
    session_id: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _graph
    from graph.builder import get_graph
    _graph = get_graph()
    log.info("FastAPI приложение запущено ✅")
    yield
    _session.clear()
    log.info("FastAPI приложение остановлено")


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/chat", response_model=QuestionResponse)
async def chat(request: QuestionRequest):
    global _graph

    session_id = request.session_id or str(uuid.uuid4())
    t_start = time.perf_counter()

    log.pipeline_start(request.data, session_id)

    state = _session.get(
        session_id,
        {"messages": []},
    )

    log.info(f"История сообщений: {len(state.get('messages', []))} шт")

    try:
        result = await _graph.ainvoke(
            {
                **state,
                "question": request.data,
            }
        )
    except Exception as e:
        elapsed = time.perf_counter() - t_start
        log.error(f"Критическая ошибка пайплайна: {type(e).__name__}: {e}")
        log.pipeline_end("Внутренняя ошибка", "True", elapsed)
        return QuestionResponse(
            answer="К сожалению, произошла внутренняя ошибка. Пожалуйста, повторите запрос позже.",
            button="",
            support="True",
            session_id=session_id,
        )

    answer = result.get("answer", "")
    support = result.get("support", "True")
    elapsed = time.perf_counter() - t_start

    log.pipeline_end(answer, support, elapsed)

    _session[session_id] = {
        "messages": result.get("messages", []),
    }

    return QuestionResponse(
        answer=answer,
        button=result.get("button") or "",
        support=support,
        session_id=session_id,
    )