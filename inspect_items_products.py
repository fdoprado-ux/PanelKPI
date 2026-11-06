import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

url = "https://api.fu.do/v1alpha1/items?page[size]=10&sort=-id&include=product"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    data = json.loads(r.read().decode('utf-8'))
    print("Items sample count:", len(data['data']))
    p_map = {}
    if 'included' in data:
        for inc in data['included']:
            if inc['type'] == 'Product':
                p_map[inc['id']] = inc['attributes']
    for it in data['data']:
        p_id = it.get('relationships', {}).get('product', {}).get('data', {}).get('id')
        prod = p_map.get(p_id, {})
        attrs = it['attributes']
        print(f"Item ID {it['id']} | Prod: {prod.get('name')} | Price: {attrs.get('price')} | Qty: {attrs.get('quantity')} | Date: {attrs.get('createdAt')}")
