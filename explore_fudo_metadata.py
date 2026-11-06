import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

def fetch(ep):
    req = urllib.request.Request(f"https://api.fu.do/v1alpha1{ep}?page[size]=50", headers=headers)
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read().decode('utf-8'))

print("=== CATEGORIES ===")
cats = fetch("/product-categories")
for c in cats['data']:
    print(c['id'], c['attributes'].get('name'))

print("\n=== PAYMENT METHODS ===")
pms = fetch("/payment-methods")
for pm in pms['data']:
    print(pm['id'], pm['attributes'].get('name'))

print("\n=== ROOMS ===")
rooms = fetch("/rooms")
for rm in rooms['data']:
    print(rm['id'], rm['attributes'].get('name'))
