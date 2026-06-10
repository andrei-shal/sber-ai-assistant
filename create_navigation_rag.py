import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


BASE_DIR = Path(__file__).parent

JOURNEYS_FILE = BASE_DIR / "journeys.json"
CHROMA_PATH = BASE_DIR / "chroma_db"

COLLECTION_NAME = "navigation_journeys"

embedding_model = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)


def build_document(journey: dict) -> str:

    keywords = journey.get("keywords", [])
    examples = journey.get("examples", [])
    path = journey.get("path", [])

    keywords_text = "\n".join(keywords)
    examples_text = "\n".join(examples)
    path_text = " → ".join(path)

    return f"""
ID:
{journey["id"]}

Название:
{journey["title"]}

Описание:
{journey["description"]}

Ключевые слова:
{keywords_text}

Примеры запросов:
{examples_text}

Путь:
{path_text}

Поисковые фразы:
{journey["title"]}
{journey["description"]}
{' '.join(keywords)}
{' '.join(examples)}
""".strip()


def main():

    with open(
        JOURNEYS_FILE,
        encoding="utf-8"
    ) as f:
        journeys = json.load(f)

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    # Полностью удаляем старую коллекцию
    try:
        client.delete_collection(
            COLLECTION_NAME
        )
        print(
            f"Deleted old collection '{COLLECTION_NAME}'"
        )
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME
    )

    ids = []
    documents = []
    embeddings = []
    metadatas = []

    for journey in journeys:

        document = build_document(
            journey
        )

        embedding = embedding_model.encode(
            f"passage: {document}",
            normalize_embeddings=True
        ).tolist()

        ids.append(
            journey["id"]
        )

        documents.append(
            document
        )

        embeddings.append(
            embedding
        )

        metadatas.append(
            {
                "journey_id": journey["id"],
                "title": journey["title"],
                "description": journey["description"],
                "path": json.dumps(
                    journey.get("path", []),
                    ensure_ascii=False
                )
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(
        f"Loaded {len(ids)} journeys into '{COLLECTION_NAME}'"
    )


if __name__ == "__main__":
    main()