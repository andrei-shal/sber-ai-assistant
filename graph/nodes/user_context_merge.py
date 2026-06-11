def user_context_merge_node(state):

    merged_context = f"""
Отфильтрованные платежи:
{state["filtered_user_context"]}

Ответ по документам относящимся к запросу:
{state["rag_context"]}
"""

    return {"merged_context": merged_context}