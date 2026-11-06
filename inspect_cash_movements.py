import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

url = "https://api.fu.do/v1alpha1/cash-movements?page[size]=10&sort=-id"
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req, context=ctx) as r:
        data = json.loads(r.read().decode('utf-8'))
        print("Cash movements count:", len(data.get('data', [])))
        for cm in data.get('data', []):
            print(json.dumps(cm, indent=2))
        if 'included' in data:
            print("Included count:", len(data['included']))
except Exception as e:
    print("Error:", e)
