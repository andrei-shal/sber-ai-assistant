from typing import TypedDict

class AgentState(TypedDict):
    messages: list

    question: str

    route: str

    answer: str
    button: str

    # RAG

    search_query: str

    documents: list

    documents_context: str

    # Nav

    nav_search_query: str

    navigation_candidates: str

    navigation_candidates_context: str