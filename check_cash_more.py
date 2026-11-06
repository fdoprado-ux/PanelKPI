import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

def check(ep):
    url = f"https://api.fu.do/v1alpha1{ep}?page[size]=5&sort=-id"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, context=ctx) as r:
            data = json.loads(r.read().decode('utf-8'))
            print(f"=== {ep} (Status: {r.status}) ===")
            print(json.dumps(data, indent=2)[:600])
    except urllib.error.HTTPError as e:
        print(f"=== {ep} HTTPError {e.code} ===")
    except Exception as e:
        print(f"=== {ep} Err {e} ===")

check("/expenses")
check("/cash-counts")
check("/cash-registers")
