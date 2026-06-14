import os
import json

import chromadb
from sentence_transformers import SentenceTransformer

_CHROMA_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "chroma_db"
)

embedding_model = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)

client = chromadb.PersistentClient(
    path=_CHROMA_DIR
)

collection = client.get_collection(
    "navigation_journeys"
)


def search(
    question: str,
    limit: int = 10
):

    embedding = embedding_model.encode(
        f"query: {question}",
        normalize_embeddings=True
    ).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=limit,
        include=[
            "documents",
            "metadatas",
            "distances"
        ]
    )

    candidates = []

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, meta, distance in zip(
        docs,
        metas,
        distances
    ):

        candidates.append(
            {
                "journey_id": meta["journey_id"],
                "title": meta["title"],
                "description": meta["description"],
                "path": json.loads(
                    meta["path"]
                ),
                "distance": distance,
                "document": doc
            }
        )

    return candidates