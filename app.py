from fastapi import FastAPI
from pydantic import BaseModel

import uuid

from graph.builder import graph

app = FastAPI()

sessions = {}

class QuestionRequest(BaseModel):
    data: str
    session_id: str | None = None

class QuestionResponse(BaseModel):
    answer: str
    button: str
    support: str
    session_id: str

print("all ok")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/chat", response_model=QuestionResponse)
async def chat(request: QuestionRequest):
    session_id = request.session_id or str(uuid.uuid4())

    state = sessions.get(
        session_id,
        {
            "messages": []
        }
    )

    print(state)

    try:
        result = await graph.ainvoke(
            {
                **state,
                "question": request.data
            }
        )
    except Exception as e:
        print(f"Ошибка при вызове графа: {e}")
        return QuestionResponse(
            answer="К сожалению, произошла внутренняя ошибка. Пожалуйста, повторите запрос позже.",
            button="",
            support="True",
            session_id=session_id
        )

    sessions[session_id] = {
        "messages": result.get(
            "messages",
            []
        )
    }

    return QuestionResponse(
        answer=result.get("answer", ""),
        button=result.get("button", ""),
        support=result.get("support", "True"),
        session_id=session_id
    )