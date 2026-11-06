import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

months = [
    ('Ene', '2026-01-01T03:00:00Z', '2026-02-01T03:00:00Z'),
    ('Feb', '2026-02-01T03:00:00Z', '2026-03-01T03:00:00Z'),
    ('Mar', '2026-03-01T03:00:00Z', '2026-04-01T03:00:00Z'),
    ('Abr', '2026-04-01T03:00:00Z', '2026-05-01T03:00:00Z'),
    ('May', '2026-05-01T03:00:00Z', '2026-06-01T03:00:00Z'),
    ('Jun', '2026-06-01T03:00:00Z', '2026-07-01T03:00:00Z'),
    ('Jul', '2026-07-01T03:00:00Z', '2026-08-01T03:00:00Z'),
    ('Ago', '2026-08-01T03:00:00Z', '2026-09-01T03:00:00Z'),
    ('Sep', '2026-09-01T03:00:00Z', '2026-10-01T03:00:00Z'),
    ('Oct', '2026-10-01T03:00:00Z', '2026-11-01T03:00:00Z'),
    ('Nov', '2026-11-01T03:00:00Z', '2026-11-06T04:00:00Z'),
]

monthly_2026 = []
year_sales = 0
year_orders = 0
year_discounts = 0

for m_name, s_iso, e_iso in months:
    page = 1
    m_sales = 0
    m_orders = 0
    m_discounts = 0
    while True:
        url = f"https://api.fu.do/v1alpha1/sales?filter[createdAt]=and(gte.{s_iso},lte.{e_iso})&page[size]=500&page[number]={page}&include=discounts"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx) as r:
            res = json.loads(r.read().decode('utf-8'))
            items = res.get('data', [])
            
            discounts_map = {}
            if 'included' in res:
                for inc in res['included']:
                    if inc['type'] == 'Discount':
                        discounts_map[inc['id']] = inc['attributes']

            for it in items:
                attrs = it['attributes']
                if attrs.get('saleState') != 'CANCELED':
                    tot = attrs.get('total', 0) or 0
                    m_sales += tot
                    m_orders += 1

                    for d_rel in it.get('relationships', {}).get('discounts', {}).get('data', []):
                        d_id = d_rel['id']
                        if d_id in discounts_map and not discounts_map[d_id].get('canceled'):
                            m_discounts += (discounts_map[d_id].get('amount') or 0)

            if len(items) < 500:
                break
            page += 1

    monthly_2026.append({
        'month': m_name,
        'sales': m_sales,
        'orders': m_orders,
        'discounts': m_discounts
    })
    year_sales += m_sales
    year_orders += m_orders
    year_discounts += m_discounts
    print(f"{m_name}: Sales=${m_sales:,.0f} CLP | Orders={m_orders} | Discounts=${m_discounts:,.0f}")

print("\n=== YEAR 2026 TOTALS ===")
print(f"Total Year 2026 Sales: ${year_sales:,.0f} CLP")
print(f"Total Year 2026 Orders: {year_orders}")
print(f"Total Year 2026 Discounts: ${year_discounts:,.0f} CLP")

with open('data_2026.json', 'w', encoding='utf-8') as f:
    json.dump({
        'monthly': monthly_2026,
        'year_sales': year_sales,
        'year_orders': year_orders,
        'year_discounts': year_discounts
    }, f, indent=2)
