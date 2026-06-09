from typing import TypedDict

class AgentState(TypedDict):
    messages: list

    question: str

    search_query: str

    documents: list

    documents_context: str

    answer: str