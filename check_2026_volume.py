import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

# Get latest sale ID and sale ID from Jan 1 2026
latest_url = "https://api.fu.do/v1alpha1/sales?page[size]=1&sort=-id"
req = urllib.request.Request(latest_url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    latest = json.loads(r.read().decode('utf-8'))['data'][0]
    print(f"Latest sale: ID {latest['id']}, Created {latest['attributes']['createdAt']}")

jan1_url = "https://api.fu.do/v1alpha1/sales?page[size]=1&filter[createdAt]=gte.2026-01-01T00:00:00Z&sort=id"
req = urllib.request.Request(jan1_url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    jan1 = json.loads(r.read().decode('utf-8'))['data'][0]
    print(f"First sale 2026: ID {jan1['id']}, Created {jan1['attributes']['createdAt']}")

total_2026_sales_approx = int(latest['id']) - int(jan1['id'])
print(f"Total sales in 2026 approximately: {total_2026_sales_approx}")
