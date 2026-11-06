import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

url = "https://api.fu.do/v1alpha1/sales?filter[createdAt]=and(gte.2026-11-05T00:00:00Z,lte.2026-11-06T23:59:59Z)&include=discounts&page[size]=50"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    data = json.loads(r.read().decode('utf-8'))

print("Discounts in sales included:")
total_discounts = 0
if 'included' in data:
    for inc in data['included']:
        if inc['type'] == 'Discount':
            attrs = inc['attributes']
            amount = attrs.get('amount', 0)
            print(f"Discount ID: {inc['id']}, amount: {amount}, canceled: {attrs.get('canceled')}")
            if not attrs.get('canceled'):
                total_discounts += amount
print(f"Total discounts today: {total_discounts}")

# Also check /discounts endpoint directly
try:
    req_disc = urllib.request.Request("https://api.fu.do/v1alpha1/discounts?page[size]=10&sort=-id", headers=headers)
    with urllib.request.urlopen(req_disc, context=ctx) as r:
        disc_direct = json.loads(r.read().decode('utf-8'))
        print("\nDirect /discounts latest sample:")
        for d in disc_direct['data']:
            print(d['id'], d['attributes'])
except Exception as e:
    print("Error querying /discounts:", e)
