from services.db import get_user_payments


def user_load_data_node(state):
    return {
        'user_data': {
            "payments": get_user_payments()
        }
    }
