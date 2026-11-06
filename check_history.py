import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

def get_sales(query):
    url = f"https://api.fu.do/v1alpha1/sales?{query}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx) as r:
        return json.loads(r.read().decode('utf-8'))

print("=== Checking Oldest Sales (to check available history) ===")
oldest = get_sales("page[size]=5&sort=createdAt")
for s in oldest['data']:
    print(f"Oldest: ID {s['id']} | Created: {s['attributes']['createdAt']} | Total: {s['attributes']['total']}")

print("\n=== Checking 2025 Sales ===")
sales_2025 = get_sales("filter[createdAt]=and(gte.2025-11-01T00:00:00Z,lte.2025-11-05T23:59:59Z)&page[size]=5")
print(f"2025 sample count: {len(sales_2025['data'])}")
for s in sales_2025['data']:
    print(f"2025: ID {s['id']} | Created: {s['attributes']['createdAt']} | Total: {s['attributes']['total']}")

print("\n=== Checking Discounts ===")
discounts = get_sales = urllib.request.Request("https://api.fu.do/v1alpha1/discounts?page[size]=10&include=sale", headers=headers)
with urllib.request.urlopen(discounts, context=ctx) as r:
    disc_data = json.loads(r.read().decode('utf-8'))
print(f"Discounts sample count: {len(disc_data['data'])}")
for d in disc_data['data']:
    print(f"Discount ID: {d['id']} | Amount: {d['attributes'].get('amount')} | Canceled: {d['attributes'].get('canceled')} | Perc: {d['attributes'].get('percentage')}")
