import urllib.request
import json
import ssl

ctx = ssl.create_default_context()

token = "eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w"

endpoints = [
    "/customers",
    "/discounts",
    "/expenses",
    "/expense-categories",
    "/ingredients",
    "/items",
    "/kitchens",
    "/payment-methods",
    "/payments",
    "/product-categories",
    "/product-modifiers",
    "/products",
    "/providers",
    "/roles",
    "/rooms",
    "/sales",
    "/subitems",
    "/tables",
    "/users"
]

base = "https://api.fu.do/v1alpha1"

for ep in endpoints:
    url = f"{base}{ep}?page[size]=1"
    req = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
    )
    try:
        with urllib.request.urlopen(req, context=ctx) as resp:
            print(f"{ep}: {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"{ep}: {e.code} - {e.reason}")
    except Exception as e:
        print(f"{ep}: {e}")
