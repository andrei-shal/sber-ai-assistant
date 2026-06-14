from services.pipeline_logger import get_logger

log = get_logger()


def user_context_builder_node(state):

    user_data = state["user_data"]

    log.info(f"SQL запрос: {state.get('user_sql', '')}")
    log.info(f"Загружено записей: {len(user_data)}")

    context = "Платежи пользователя:\n\n"

    for payment in user_data:

        context += f"""
ID отправителя: {payment.get("company_id")}
ID получателя: {payment.get("receiver_id")}
Сумма: {payment.get("amount")}
Статус: {payment.get("status")}
timestamp: {payment.get("timestamp")}
---
"""

    return {
        "user_context": context
    }