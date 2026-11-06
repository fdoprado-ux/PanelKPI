import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

print("Testing /sales?filter[paymentMethodId]=eq.1 ...")
url = "https://api.fu.do/v1alpha1/sales?filter[paymentMethodId]=eq.1&filter[createdAt]=gte.2026-10-01T00:00:00Z&page[size]=5"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    data = json.loads(r.read().decode('utf-8'))
    print(f"Sales with paymentMethodId=1: count={len(data['data'])}")
    for s in data['data']:
        print(f"Sale ID {s['id']} | Total: {s['attributes']['total']} | Date: {s['attributes']['createdAt']}")

print("\nTesting /payments with filter[createdAt]...")
url_p = "https://api.fu.do/v1alpha1/payments?filter[createdAt]=gte.2026-10-01T00:00:00Z&page[size]=5"
req_p = urllib.request.Request(url_p, headers=headers)
with urllib.request.urlopen(req_p, context=ctx) as r:
    data_p = json.loads(r.read().decode('utf-8'))
    print(f"Payments in range: count={len(data_p['data'])}")
