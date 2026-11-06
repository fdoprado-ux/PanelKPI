import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

req = urllib.request.Request('https://api.fu.do/v1alpha1/sales?page[size]=10&sort=-closedAt&include=discounts', headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    data = json.loads(r.read().decode('utf-8'))

print("Sales count in sample:", len(data['data']))
for s in data['data']:
    attrs = s['attributes']
    print(f"ID: {s['id']} | Closed: {attrs.get('closedAt')} | Created: {attrs.get('createdAt')} | State: {attrs.get('saleState')} | Total: {attrs.get('total')}")

if 'included' in data:
    print(f"\nIncluded objects count: {len(data['included'])}")
    for inc in data['included'][:5]:
        print(f"Included: Type: {inc.get('type')} | ID: {inc.get('id')} | Attrs: {inc.get('attributes')}")
