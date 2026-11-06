import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

url = "https://api.fu.do/v1alpha1/payments?page[size]=10&sort=-id&include=paymentMethod"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    data = json.loads(r.read().decode('utf-8'))
    print("Payments sample count:", len(data['data']))
    pm_map = {}
    if 'included' in data:
        for inc in data['included']:
            if inc['type'] == 'PaymentMethod':
                pm_map[inc['id']] = inc['attributes']['name']
    for p in data['data']:
        pm_id = p.get('relationships', {}).get('paymentMethod', {}).get('data', {}).get('id')
        pm_name = pm_map.get(pm_id, f"ID {pm_id}")
        attrs = p['attributes']
        print(f"Payment ID {p['id']} | Amount: {attrs.get('amount')} | Date: {attrs.get('createdAt')} | Method: {pm_name}")
