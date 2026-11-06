import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
req = urllib.request.Request('https://api.fu.do/v1alpha1/users', headers={'Authorization': f'Bearer {token}', 'Accept': 'application/json'})
with urllib.request.urlopen(req, context=ctx) as r:
    data = json.loads(r.read().decode('utf-8'))
for u in data['data']:
    attrs = u['attributes']
    role_id = u['relationships']['role']['data']['id'] if u['relationships'].get('role') and u['relationships']['role'].get('data') else 'None'
    print(f"ID: {u['id']:<4} Name: {attrs.get('name',''):<20} Email: {str(attrs.get('email','')):<25} Active: {attrs.get('active')} Role: {role_id}")
