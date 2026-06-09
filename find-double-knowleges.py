from pathlib import Path
import hashlib
from collections import defaultdict


KNOWLEDGE_DIR = Path("knowledge")


def file_hash(path):
    sha = hashlib.sha256()

    with open(path, "rb") as f:
        while chunk := f.read(8192):
            sha.update(chunk)

    return sha.hexdigest()


duplicates = defaultdict(list)

for file in KNOWLEDGE_DIR.rglob("*"):

    if not file.is_file():
        continue

    file_hash_value = file_hash(file)

    duplicates[file_hash_value].append(file)

found = False

for hash_value, files in duplicates.items():

    if len(files) < 2:
        continue

    found = True

    print("\n" + "=" * 80)
    print(f"Дубликат ({len(files)} файлов)")
    print("=" * 80)

    for file in files:
        print(file)

if not found:
    print("Дубликаты не найдены")