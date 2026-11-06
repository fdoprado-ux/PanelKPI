import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

url = "https://api.fu.do/v1alpha1/cash-counts?page[size]=5&sort=-id"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req, context=ctx) as r:
    data = json.loads(r.read().decode('utf-8'))
for cc in data['data']:
    attrs = cc['attributes']
    print(f"ID {cc['id']} | Opened: {attrs.get('openedAt')} | Closed: {attrs.get('closedAt')} | Init: {attrs.get('init')} | Income: {attrs.get('income')} | Expenditure: {attrs.get('expenditure')}")
    print("ExpenditureDetail:", attrs.get('expenditureDetail'))
    print("IncomeDetail:", attrs.get('incomeDetail'))
    print("-" * 50)
