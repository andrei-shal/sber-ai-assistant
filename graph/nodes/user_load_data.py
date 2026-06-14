from services.db import query_payments


def user_load_data_node(state):
    return {
        'user_data': query_payments(state['user_sql']),
    }
