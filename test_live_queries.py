import urllib.request, json, ssl, time
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

def query_sales_range(label, start_iso, end_iso):
    t0 = time.time()
    url = f"https://api.fu.do/v1alpha1/sales?filter[createdAt]=and(gte.{start_iso},lte.{end_iso})&page[size]=500"
    req = urllib.request.Request(url, headers=headers)
    total_sales = 0
    orders = 0
    page = 1
    while True:
        p_url = f"{url}&page[number]={page}"
        p_req = urllib.request.Request(p_url, headers=headers)
        with urllib.request.urlopen(p_req, context=ctx) as r:
            res = json.loads(r.read().decode('utf-8'))
            items = res.get('data', [])
            for it in items:
                if it['attributes'].get('saleState') != 'CANCELED':
                    total_sales += it['attributes'].get('total', 0)
                    orders += 1
            if len(items) < 500:
                break
            page += 1
    elapsed = time.time() - t0
    print(f"{label}: Orders={orders}, Total=${total_sales:,.0f} CLP (Took {elapsed:.2f}s, {page} pages)")
    return {'orders': orders, 'total': total_sales}

print("Testing live queries...")
# Today (Nov 5 00:00 to Nov 6 23:59 UTC)
query_sales_range("Today (Nov 5-6)", "2026-11-05T00:00:00Z", "2026-11-06T23:59:59Z")

# Last 7 Days (Oct 30 to Nov 5)
query_sales_range("Last 7 Days", "2026-10-30T00:00:00Z", "2026-11-05T23:59:59Z")

# Same month (Nov 1 to Nov 5) in 2025
query_sales_range("Nov 1-5 2025", "2025-11-01T00:00:00Z", "2025-11-05T23:59:59Z")

# Same month (Nov 1 to Nov 5) in 2024
query_sales_range("Nov 1-5 2024", "2024-11-01T00:00:00Z", "2024-11-05T23:59:59Z")

# Same month (Nov 1 to Nov 5) in 2023
query_sales_range("Nov 1-5 2023", "2023-11-01T00:00:00Z", "2023-11-05T23:59:59Z")
