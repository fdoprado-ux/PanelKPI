import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

def test_query(q):
    url = f"https://api.fu.do/v1alpha1/cash-counts?{q}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            data = json.loads(r.read().decode('utf-8'))
            print(f"Query '{q}': Status {r.status}, Count: {len(data['data'])}")
            if data['data']:
                attrs = data['data'][0]['attributes']
                print(f"Sample: ID {data['data'][0]['id']}, openedAt {attrs.get('openedAt')}, expenditure {attrs.get('expenditure')}")
    except urllib.error.HTTPError as e:
        print(f"Query '{q}' FAILED: {e.code} - {e.read().decode('utf-8')[:200]}")

test_query("page[size]=5&sort=-id")
test_query("filter[openedAt]=gte.2026-11-01T00:00:00Z&page[size]=5")
test_query("filter[openedAt]=gte.2026-01-01T00:00:00Z&page[size]=100")
