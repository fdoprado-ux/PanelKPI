import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

def test_ep(name, path):
    url = f"https://api.fu.do/v1alpha1{path}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            data = json.loads(r.read().decode('utf-8'))
            print(f"=== {name} ({r.status}) ===")
            if 'data' in data:
                print(f"Count: {len(data['data'])}")
                if len(data['data']) > 0:
                    print("Sample item:", json.dumps(data['data'][0], indent=2)[:400])
            else:
                print("Response:", str(data)[:300])
    except urllib.error.HTTPError as e:
        print(f"=== {name} ERROR {e.code} ===")
        print(e.read().decode('utf-8')[:300])
    except Exception as e:
        print(f"=== {name} EXCEPTION ===", e)

# Test cash movements
test_ep("Cash Movements", "/cash-movements?page[size]=5")

# Test payments
test_ep("Payments", "/payments?page[size]=5")

# Test items
test_ep("Items", "/items?page[size]=5")

# Test sales with paymentMethodId filter
test_ep("Sales Cash filter", "/sales?filter[paymentMethodId]=eq.1&page[size]=5")
