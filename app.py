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

    result = await graph.ainvoke(
        {
            **state,
            "question": request.data
        }
    )

    sessions[session_id] = {
        "messages": result.get(
            "messages",
            []
        )
    }

    return QuestionResponse(
        answer=result["answer"],
        button=result["button"],
        support=result["support"],
        session_id=session_id
    )