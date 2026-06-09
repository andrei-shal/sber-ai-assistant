from pathlib import Path

import chromadb

from pypdf import PdfReader
from docx import Document

import hashlib

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "intfloat/multilingual-e5-base"
)

def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(
            f.read()
        ).hexdigest()

def load_pdf(path):
    reader = PdfReader(path)

    return "\n".join(
        page.extract_text() or ""
        for page in reader.pages
    )


def load_docx(path):
    doc = Document(path)

    return "\n".join(
        paragraph.text
        for paragraph in doc.paragraphs
    )

def load_md(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_text(text, chunk_size=1200, overlap=200):
    chunks = []

    start = 0

    while start < len(text):
        end = start + chunk_size

        chunks.append(text[start:end])

        start += chunk_size - overlap

    return chunks


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="bank_knowledge"
)

knowledge_dir = Path("knowledge")

for file in knowledge_dir.rglob("*"):

    if not file.is_file():
        continue

    hash_value = file_hash(file)

    existing = collection.get(
        where={"source": str(file)}
    )

    if existing["metadatas"]:
        old_hash = existing["metadatas"][0]["hash"]

        if old_hash == hash_value:
            print(f"Без изменений: {file}")
            continue

    existing = collection.get(
        where={"hash": hash_value}
    )

    if existing["ids"]:
        print(f"Дубликат: {file}")
        continue

    collection.delete(
        where={"source": str(file)}
    )

    suffix = file.suffix.lower()

    if suffix == ".pdf":
        text = load_pdf(file)

    elif suffix == ".docx":
        text = load_docx(file)

    elif suffix == ".md" or suffix == ".MD":
        text = load_md(file)

    else:
        continue

    if not text.strip():
        print(f"Пустой файл: {file}")
        continue

    chunks = [
        chunk.strip()
        for chunk in split_text(text)
        if chunk.strip()
    ]

    relative_path = file.relative_to(knowledge_dir)

    path_context = " > ".join(relative_path.parts[:-1])

    title = file.stem.replace("_", " ")

    chunks = [
    f"""passage:  {title}.
Документ относится к категории {relative_path.parts[0]}
{", подкатегори " + relative_path.parts[1] if len(relative_path.parts) > 1 else ""}

{chunk}"""
        for chunk in chunks
    ]

    embeddings = model.encode(
        chunks,
        normalize_embeddings=True
    ).tolist()

    ids = [
        f"{hash_value}_{idx}"
        for idx in range(len(chunks))
    ]

    metadatas = [
        {
            "source": str(file),
            "hash": hash_value,
            "path": "/".join(relative_path.parts[:-1]),
            "category": relative_path.parts[0] if len(relative_path.parts) > 0 else "",
            "filename": file.name
        }
        for _ in chunks
    ]

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=ids,
        metadatas=metadatas
    )

    print(f"Загружен: {file}")

print("Готово")