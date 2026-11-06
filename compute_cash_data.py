import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

print("=== CALCULATING CASH WITHDRAWALS (RETIROS / EXPENDITURE) FROM CASH COUNTS ===")

# Periods
periods = {
    'today': ('2026-11-05T12:00:00Z', '2026-11-06T23:59:59Z'),
    'week': ('2026-10-30T00:00:00Z', '2026-11-06T23:59:59Z'),
    'month': ('2026-10-01T00:00:00Z', '2026-10-31T23:59:59Z'),
    'year': ('2026-01-01T00:00:00Z', '2026-11-06T23:59:59Z')
}

# Fetch all 2026 cash counts
all_cash_counts = []
page = 1
while True:
    url = f"https://api.fu.do/v1alpha1/cash-counts?filter[openedAt]=gte.2026-01-01T00:00:00Z&page[size]=500&page[number]={page}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, context=ctx) as r:
        res = json.loads(r.read().decode('utf-8'))
        items = res.get('data', [])
        all_cash_counts.extend(items)
        if len(items) < 500: break
        page += 1

print(f"Total Cash Counts in 2026: {len(all_cash_counts)}")

withdrawals = {'today': 0, 'week': 0, 'month': 0, 'year': 0}
withdrawals_counts = {'today': 0, 'week': 0, 'month': 0, 'year': 0}

cash_sales = {'today': 0, 'week': 0, 'month': 0, 'year': 0}
cash_orders = {'today': 0, 'week': 0, 'month': 0, 'year': 0}

for cc in all_cash_counts:
    attrs = cc['attributes']
    if attrs.get('canceled'): continue
    o_at = attrs.get('openedAt', '')
    exp = attrs.get('expenditure', 0) or 0
    
    # Check incomeDetail for cash payments
    inc_detail = attrs.get('incomeDetail') or {}
    cash_pay = 0
    if isinstance(inc_detail, dict) and '1' in inc_detail:
        c1 = inc_detail['1']
        if isinstance(c1, dict):
            cash_pay = (c1.get('payments') or 0) + (c1.get('tip') or 0)

    # Year
    withdrawals['year'] += exp
    if exp > 0: withdrawals_counts['year'] += 1
    cash_sales['year'] += cash_pay

    # Month (Oct 2026)
    if '2026-10-01' <= o_at[:10] <= '2026-10-31':
        withdrawals['month'] += exp
        if exp > 0: withdrawals_counts['month'] += 1
        cash_sales['month'] += cash_pay

    # Week (Oct 30 to Nov 6)
    if '2026-10-30' <= o_at[:10] <= '2026-11-06':
        withdrawals['week'] += exp
        if exp > 0: withdrawals_counts['week'] += 1
        cash_sales['week'] += cash_pay

    # Today (Nov 5 - 6 shift)
    if o_at[:10] in ['2026-11-05', '2026-11-06']:
        withdrawals['today'] += exp
        if exp > 0: withdrawals_counts['today'] += 1
        cash_sales['today'] += cash_pay

print("\n--- RETIROS DE CAJA (EXPENDITURES) ---")
print(f"Hoy: ${withdrawals['today']:,.0f} CLP ({withdrawals_counts['today']} retiros)")
print(f"Semana Pasada: ${withdrawals['week']:,.0f} CLP ({withdrawals_counts['week']} retiros)")
print(f"Mes Pasado (Oct): ${withdrawals['month']:,.0f} CLP ({withdrawals_counts['month']} retiros)")
print(f"Año 2026: ${withdrawals['year']:,.0f} CLP ({withdrawals_counts['year']} retiros)")

print("\n--- VENTAS MEDIO DE PAGO EFECTIVO ---")
print(f"Hoy: ${cash_sales['today']:,.0f} CLP")
print(f"Semana Pasada: ${cash_sales['week']:,.0f} CLP")
print(f"Mes Pasado (Oct): ${cash_sales['month']:,.0f} CLP")
print(f"Año 2026: ${cash_sales['year']:,.0f} CLP")

with open('cash_data.json', 'w', encoding='utf-8') as f:
    json.dump({
        'withdrawals': withdrawals,
        'withdrawals_counts': withdrawals_counts,
        'cash_sales': cash_sales
    }, f, indent=2)
