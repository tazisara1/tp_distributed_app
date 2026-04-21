from dataclasses import dataclass
from typing import List, Optional
import json
from datetime import datetime
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
    
def validate_user(user: dict):
     if not isinstance(user.get("username"), str) or not (3 <= len(user["username"]) <= 30):
        raise ValueError("username invalide")

     if not user["username"].replace("_", "").isalnum():
        raise ValueError("username format invalide")

     if not isinstance(user.get("display_name"), str) or not (1 <= len(user["display_name"]) <= 100):
        raise ValueError("display_name invalide")

     if user.get("role") not in ["viewer", "editor", "admin"]:
        raise ValueError("role invalide")

def validate_document(doc: dict):
    if not isinstance(doc.get("id"), int) or doc["id"] <= 0:
        raise ValueError("id invalide")

    if not isinstance(doc.get("title"), str) or not (1 <= len(doc["title"].strip()) <= 200):
        raise ValueError("title invalide")

    if not isinstance(doc.get("author"), str) or not (1 <= len(doc["author"]) <= 100):
        raise ValueError("author invalide")

    if "tags" in doc:
        if not isinstance(doc["tags"], list) or len(doc["tags"]) > 20:
            raise ValueError("tags invalides")
        for t in doc["tags"]:
            if not (1 <= len(t) <= 50):
                raise ValueError("tag invalide")

    if "classification" in doc:
        if doc["classification"] not in ["public", "internal", "confidential", "secret"]:
            raise ValueError("classification invalide")

    if "created_at" in doc:
        try:
            datetime.fromisoformat(doc["created_at"].replace("Z", ""))
        except:
            raise ValueError("date invalide")

def deserialize(json_str: str) -> Document:
    data = json.loads(json_str)

    validate_user(data["user"])
    validate_document(data)

    user = UserPublic(**data["user"])

    return Document(
        id=data["id"],
        title=data["title"],
        author=data["author"],
        user=user,
        tags=data.get("tags"),
        classification=data.get("classification", "internal"),
        created_at=data.get("created_at")
    )
def serialize(doc: Document) -> str:
    data = {
        "id": doc.id,
        "title": doc.title,
        "author": doc.author,
        "user": {
            "username": doc.user.username,
            "display_name": doc.user.display_name,
            "role": doc.user.role
        },
        "tags": doc.tags,
        "classification": doc.classification,
        "created_at": doc.created_at
    }

    return json.dumps(data)
if __name__ == "__main__":
    # ✅ VALIDE
    json_valid = '''
    {
        "id": 1,
        "title": "Rapport",
        "author": "Alice",
        "user": {
            "username": "alice_1",
            "display_name": "Alice Dupont",
            "role": "editor"
        }
    }
    '''

    doc = deserialize(json_valid)
    print(serialize(doc))


    # ❌ id invalide
    try:
        bad = '{"id": -1, "title":"ok","author":"a","user":{"username":"abc","display_name":"x","role":"viewer"}}'
        deserialize(bad)
    except Exception as e:
        print(e)


    # ❌ role invalide
    try:
        bad = '{"id": 1, "title":"ok","author":"a","user":{"username":"abc","display_name":"x","role":"boss"}}'
        deserialize(bad)
    except Exception as e:
        print(e)


    # ❌ title vide
    try:
        bad = '{"id": 1, "title":"", "author":"a","user":{"username":"abc","display_name":"x","role":"viewer"}}'
        deserialize(bad)
    except Exception as e:
        print(e)


    # ❌ tag trop long
    try:
        bad = '''
        {
            "id": 1,
            "title": "ok",
            "author": "a",
            "tags": ["aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"],
            "user": {"username":"abc","display_name":"x","role":"viewer"}
        }
        '''
        deserialize(bad)
    except Exception as e:
        print(e) 
