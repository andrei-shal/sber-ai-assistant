def nav_build_context_node(state):

    navigation_context = ""

    for candidate in state["navigation_candidates"]:

        if candidate["distance"] < 0.3:

            path = " → ".join(
                candidate["path"]
            )

            navigation_context += f"""
ID: {candidate["journey_id"]}

Название:
{candidate["title"]}

Описание:
{candidate["description"]}

Путь:
{path}

---
"""

    return {
        "navigation_candidates_context": navigation_context
    }