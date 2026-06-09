import chromadb

from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)

chroma = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = chroma.get_collection(
    name="bank_knowledge"
)

def search(
    question: str,
    limit: int = 5
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

    result = []

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    for doc, meta, distance in zip(
        docs,
        metas,
        distances
    ):

        source = meta.get(
            "relative_path",
            meta.get(
                "source",
                "unknown"
            )
        )

        meta_hash = meta.get("hash", "unknown")

        result.append({
            "source": source,
            "document": doc,
            "distance": distance,
            "hash": meta_hash,
        })

    return result