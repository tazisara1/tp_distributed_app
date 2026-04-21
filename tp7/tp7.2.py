import json
from dataclasses import dataclass
from typing import List

DEFAULT_TAGS = []
DEFAULT_CLASSIFICATION = "internal"
ALLOWED_CLASSIFICATION = {"public", "internal", "confidential", "secret"}


@dataclass
class Document:
    id: int
    title: str
    author: str
    tags: List[str]
    classification: str


def validate(doc: Document):
    if not isinstance(doc.id, int) or doc.id <= 0:
        return "id invalide"

    if not isinstance(doc.title, str) or not doc.title.strip():
        return "title invalide"

    if not isinstance(doc.author, str) or not doc.author.strip():
        return "author invalide"

    if not isinstance(doc.tags, list):
        return "tags invalide"

    if doc.classification not in ALLOWED_CLASSIFICATION:
        return "classification invalide"

    return None


def deserialize_document(raw: str) -> Document:
    data = json.loads(raw)

    doc = Document(
        id=data.get("id"),
        title=data.get("title"),
        author=data.get("author"),
        tags=data.get("tags", DEFAULT_TAGS),
        classification=data.get("classification", DEFAULT_CLASSIFICATION)
    )

    error = validate(doc)
    if error:
        raise ValueError(f"Validation échouée: {error}")

    return doc


def test():
    v1 = '{"id":1,"title":"Rapport","author":"Alice"}'

    v2 = '{"id":2,"title":"Note","author":"Bob","tags":["finance"],"classification":"public"}'

    invalid = '{"id":3,"title":"X","author":"A","classification":"top_secret"}'

    unknown = '{"id":4,"title":"X","author":"A","priority":"urgent"}'

    cases = [v1, v2, invalid, unknown]

    for i, c in enumerate(cases):
        print("\n--- case", i+1, "---")
        try:
            print(deserialize_document(c))
        except Exception as e:
            print("REJECTED:", e)


if __name__ == "__main__":
    test()