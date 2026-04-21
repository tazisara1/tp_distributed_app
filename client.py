import urllib.request
import urllib.error
import json

BASE_URL = "http://127.0.0.1:8080"
TOKEN = "secret-token-abc123"

print("=" * 40)
print("TEST 1 : GET /health (sans authentification)")
print("=" * 40)
req = urllib.request.urlopen(f"{BASE_URL}/health")
print(json.loads(req.read()))

print("\n" + "=" * 40)
print("TEST 2 : POST /documents (avec token valide)")
print("=" * 40)
body = json.dumps({"title": "Mon document", "content": "Contenu du document"}).encode()
req = urllib.request.Request(
    f"{BASE_URL}/documents",
    data=body,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    },
    method="POST"
)
print(json.loads(urllib.request.urlopen(req).read()))

print("\n" + "=" * 40)
print("TEST 3 : POST sans token → erreur 401")
print("=" * 40)
try:
    req = urllib.request.Request(
        f"{BASE_URL}/documents",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    urllib.request.urlopen(req)
except urllib.error.HTTPError as e:
    print(json.loads(e.read()))

print("\n" + "=" * 40)
print("TEST 4 : GET /inconnu → erreur 404")
print("=" * 40)
try:
    urllib.request.urlopen(f"{BASE_URL}/inconnu")
except urllib.error.HTTPError as e:
    print(json.loads(e.read()))
