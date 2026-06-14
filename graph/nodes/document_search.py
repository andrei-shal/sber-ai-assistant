from services.pipeline_logger import get_logger
import hashlib

from services.rag import search

log = get_logger()

def document_search_node(state):
    queries = [
        q.strip()
        for q in state["search_query"].split(";")
        if q.strip()
    ][:5]

    all_results = []
    for query in queries:
        results = search(query, limit=20)
        all_results.extend(results)

    all_results.sort(key=lambda x: x["distance"])

    unique_results = uniqueize(all_results)

    for result in unique_results[:10]:
        log.info(f"  📄 dist={result['distance']:.4f} | {result['source']}")

    log.info(f"Всего найдено документов: {len(unique_results)}")

    return {
        "documents": unique_results
    }

def uniqueize(data: list):
    seen = set()
    result = []

    for row in data:
        key = (row["hash"], hashlib.md5(
            row["document"].encode()
        ).hexdigest())

        if key in seen:
            continue

        seen.add(key)
        result.append(row)

    return result