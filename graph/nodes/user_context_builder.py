def user_context_builder_node(state):

    user_data = state["user_data"]

    print(user_data)
    print(state["user_sql"])

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