from typing import TypedDict, Annotated


def merge_strings(current: str | None, new: str | None) -> str:
    return new if new else (current or "")

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

    # User data

    user_data: dict

    user_context: str

    filtered_user_context: Annotated[str, merge_strings]

    rag_context: Annotated[str, merge_strings]

    merged_context: str