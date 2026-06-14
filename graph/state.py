from typing import TypedDict, Annotated

class AgentState(TypedDict, total=False):
    messages: list

    question: str

    route: str

    answer: str
    button: str
    support: str

    button_correct: bool

    # RAG

    search_query: str

    documents: list

    documents_context: str

    # Nav

    nav_search_query: str

    navigation_candidates: list

    navigation_candidates_context: str

    # User data

    user_sql: str

    user_data: list

    user_context: str