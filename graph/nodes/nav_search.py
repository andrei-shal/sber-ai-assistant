from services.nav_rag import search

def nav_search_node(state):

    print(state["nav_search_query"])
    queries = [
        state["nav_search_query"]
    ]

    all_results = []

    for query in queries:
        all_results.extend(
            search(
                query,
                limit=10
            )
        )

    unique = {}

    for item in all_results:

        journey_id = item["journey_id"]

        if (
            journey_id not in unique
            or item["distance"] < unique[journey_id]["distance"]
        ):
            unique[journey_id] = item

    results = sorted(
        unique.values(),
        key=lambda x: x["distance"]
    )

    print(results[:10])

    return {
        "navigation_candidates": results[:10]
    }