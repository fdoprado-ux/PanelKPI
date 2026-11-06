import urllib.request
import json
import ssl

ctx = ssl.create_default_context()

apiKey = "MTIzQDQ1NTIz"
apiSecret = "tc1n4DbzuQ3NdzgjHFTNDAs2mihP78P1"

url = "https://auth.fu.do/api"
data = json.dumps({"apiKey": apiKey, "apiSecret": apiSecret}).encode('utf-8')

req = urllib.request.Request(
    url,
    data=data,
    headers={
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "Dashboard-Steakout/1.0"
    }
)

try:
    with urllib.request.urlopen(req, context=ctx) as response:
        res_body = response.read().decode('utf-8')
        print("Auth Response:", res_body)
        token_data = json.loads(res_body)
        token = token_data.get("token")
        print("Token received! Token length:", len(token) if token else 0)

        # Let's test a GET to /sales with this token
        sales_req = urllib.request.Request(
            "https://api.fu.do/v1alpha1/sales?page[size]=5",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "User-Agent": "Dashboard-Steakout/1.0"
            }
        )
        with urllib.request.urlopen(sales_req, context=ctx) as sales_resp:
            sales_body = sales_resp.read().decode('utf-8')
            print("Sales status:", sales_resp.status)
            sales_json = json.loads(sales_body)
            print("Sales data sample keys:", list(sales_json.keys()) if isinstance(sales_json, dict) else len(sales_json))
            print("Sales sample:", json.dumps(sales_json, indent=2)[:500])
except Exception as e:
    print("Error:", e)
    if hasattr(e, 'read'):
        print("Error details:", e.read().decode('utf-8'))
