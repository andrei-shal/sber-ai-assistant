def after_retrieve(state):

    if state["context"]:
        return "answer"

    return "rewrite"