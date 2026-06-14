from services.pipeline_logger import get_logger
from services.nav_rag import search

log = get_logger()

def nav_search_node(state):

    log.info(f"nav search query: {state['nav_search_query']}")
    queries = [
        q.strip()
        for q in state["nav_search_query"].split(";")
        if q.strip()
    ][:5]

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

    for r in results[:10]:
        log.info(f"  🧭 dist={r['distance']:.4f} | {r['title']} ({r['journey_id']})")

    return {
        "navigation_candidates": results[:10]
    }