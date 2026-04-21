from dataclasses import dataclass
from typing import List, Optional
import json
import re
from datetime import datetime

# -------------------------
# DATA CLASSES
# -------------------------

@dataclass
class UserPublic:
    username: str
    display_name: str
    role: str


@dataclass
class Document:
    id: int
    title: str
    author: str
    user: UserPublic
    tags: Optional[List[str]] = None
    classification: str = "internal"
    created_at: Optional[str] = None


# -------------------------
# CONSTANTS
# -------------------------

ROLES = {"viewer", "editor", "admin"}
CLASSIFICATIONS = {"public", "internal", "confidential", "secret"}


# -------------------------
# VALIDATION
# -------------------------

def validate_user(user: UserPublic):
    if not isinstance(user.username, str) or not re.fullmatch(r"[A-Za-z0-9_]{3,30}", user.username):
        return "username invalide"

    if not isinstance(user.display_name, str) or not (1 <= len(user.display_name.strip()) <= 100):
        return "display_name invalide"

    if user.role not in ROLES:
        return "role invalide"

    return None


def validate_document(doc: Document):
    if not isinstance(doc.id, int) or doc.id <= 0:
        return "id invalide"

    if not isinstance(doc.title, str) or not (1 <= len(doc.title.strip()) <= 200):
        return "title invalide"

    if not isinstance(doc.author, str) or not (1 <= len(doc.author.strip()) <= 100):
        return "author invalide"

    if doc.classification not in CLASSIFICATIONS:
        return "classification invalide"

    if doc.tags is not None:
        if not isinstance(doc.tags, list) or len(doc.tags) > 20:
            return "tag invalide"
        for t in doc.tags:
            if not isinstance(t, str) or not (1 <= len(t) <= 50):
                return "tag invalide"

    if doc.created_at is not None:
        try:
            datetime.strptime(doc.created_at, "%Y-%m-%dT%H:%M:%SZ")
        except:
            return "created_at invalide"

    return validate_user(doc.user)


# -------------------------
# SERIALIZE
# -------------------------

def serialize_document(doc: Document) -> str:
    return json.dumps(doc, default=lambda o: o.__dict__)


# -------------------------
# DESERIALIZE (FAIL CLOSED)
# -------------------------

def deserialize_document(raw: str) -> Document:
    data = json.loads(raw)

    user_data = data.get("user", {})

    user = UserPublic(
        username=user_data.get("username"),
        display_name=user_data.get("display_name"),
        role=user_data.get("role")
    )

    doc = Document(
        id=data.get("id"),
        title=data.get("title"),
        author=data.get("author"),
        user=user,
        tags=data.get("tags"),
        classification=data.get("classification", "internal"),
        created_at=data.get("created_at")
    )

    error = validate_document(doc)
    if error:
        raise ValueError(f"Validation échouée: {error}")

    return doc


# -------------------------
# TESTS
# -------------------------

def run_tests():
    cases = [
        {
            "name": "valid1",
            "data": {
                "id": 1,
                "title": "Rapport",
                "author": "Alice",
                "user": {"username": "alice_1", "display_name": "Alice Dupont", "role": "editor"},
                "tags": None,
                "classification": "internal",
                "created_at": None
            }
        },
        {
            "name": "valid2",
            "data": {
                "id": 2,
                "title": "Note",
                "author": "Bob",
                "user": {"username": "bob_2", "display_name": "Bob Martin", "role": "viewer"}
            }
        },
        {
            "name": "invalid_id",
            "data": {
                "id": -5,
                "title": "X",
                "author": "Bob",
                "user": {"username": "bob_2", "display_name": "Bob", "role": "viewer"}
            }
        },
        {
            "name": "invalid_role",
            "data": {
                "id": 1,
                "title": "X",
                "author": "Bob",
                "user": {"username": "bob_2", "display_name": "Bob", "role": "hacker"}
            }
        },
        {
            "name": "invalid_tag",
            "data": {
                "id": 1,
                "title": "X",
                "author": "Bob",
                "user": {"username": "bob_2", "display_name": "Bob", "role": "viewer"},
                "tags": ["x" * 100]
            }
        }
    ]

    for c in cases:
        print("\n---", c["name"], "---")
        try:
            obj = deserialize_document(json.dumps(c["data"]))
            print("OK:", obj)
        except Exception as e:
            print("REJECTED:", e)


if __name__ == "__main__":
    run_tests()