from services.db import get_user_payments, query_payments


def user_load_data_node(state):
    return {
        'user_data': query_payments(state['user_sql']),
    }
