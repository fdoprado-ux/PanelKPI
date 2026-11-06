import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
token = "eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w"

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

def get(path):
    req = urllib.request.Request(f"https://api.fu.do/v1alpha1{path}", headers=headers)
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read().decode('utf-8'))

print("=== USERS ===")
users = get("/users")
print(json.dumps(users, indent=2))

print("\n=== ROLES ===")
roles = get("/roles")
print(json.dumps(roles, indent=2))
