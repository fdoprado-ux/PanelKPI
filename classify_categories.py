import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

req = urllib.request.Request("https://api.fu.do/v1alpha1/product-categories?page[size]=100", headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    cats = json.loads(r.read().decode('utf-8'))['data']

kitchen_cats = []
bar_cats = []

for c in cats:
    cid = c['id']
    name = c['attributes']['name']
    name_l = name.lower()
    if any(k in name_l for k in ['cerveza', 'coctel', 'pisco', 'vodka', 'whisky', 'ron', 'vino', 'tequila', 'gin', 'licor', 'bebida', 'sin alcohol', 'cafeteria', 'por copa', 'shots', 'liquidos', 'carmenere', 'merlot', 'cabernet']):
        bar_cats.append((cid, name))
    else:
        kitchen_cats.append((cid, name))

print("=== BAR / LIQUIDS CATEGORIES ===")
for cid, name in bar_cats:
    print(f"ID {cid:2}: {name}")

print("\n=== KITCHEN / FOOD CATEGORIES ===")
for cid, name in kitchen_cats:
    print(f"ID {cid:2}: {name}")
