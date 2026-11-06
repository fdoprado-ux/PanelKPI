import urllib.request, json, ssl, time
from datetime import datetime, timedelta

ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

def fetch_period(start_iso, end_iso, include_discounts=True):
    page = 1
    total_sales = 0.0
    total_discounts = 0.0
    orders = 0
    sales_by_day = {}
    channel_counts = {'EAT-IN': 0, 'DELIVERY': 0, 'TAKEAWAY': 0}

    while True:
        inc = "&include=discounts" if include_discounts else ""
        url = f"https://api.fu.do/v1alpha1/sales?filter[createdAt]=and(gte.{start_iso},lte.{end_iso})&page[size]=500&page[number]={page}{inc}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=ctx) as r:
            res = json.loads(r.read().decode('utf-8'))
            items = res.get('data', [])
            
            # Extract included discounts map
            discounts_map = {}
            if 'included' in res:
                for inc_item in res['included']:
                    if inc_item['type'] == 'Discount':
                        discounts_map[inc_item['id']] = inc_item['attributes']

            for s in items:
                attrs = s['attributes']
                if attrs.get('saleState') != 'CANCELED':
                    tot = attrs.get('total', 0) or 0
                    total_sales += tot
                    orders += 1

                    # Channel
                    stype = attrs.get('saleType', 'EAT-IN')
                    if stype in channel_counts:
                        channel_counts[stype] += 1
                    else:
                        channel_counts['EAT-IN'] += 1

                    # Date aggregation
                    c_at = attrs.get('createdAt', '')[:10]
                    sales_by_day[c_at] = sales_by_day.get(c_at, 0) + tot

                    # Discounts
                    rels = s.get('relationships', {}).get('discounts', {}).get('data', [])
                    for d_rel in rels:
                        d_id = d_rel['id']
                        if d_id in discounts_map:
                            d_attr = discounts_map[d_id]
                            if not d_attr.get('canceled'):
                                total_discounts += (d_attr.get('amount') or 0)

            if len(items) < 500:
                break
            page += 1

    return {
        'total_sales': total_sales,
        'orders': orders,
        'avg_ticket': round(total_sales / orders) if orders > 0 else 0,
        'total_discounts': total_discounts,
        'sales_by_day': sales_by_day,
        'channels': channel_counts
    }

print("1. Fetching Today (Nov 5 - 6)...")
res_today = fetch_period("2026-11-05T03:00:00Z", "2026-11-06T04:00:00Z")
print(f"Today: Sales=${res_today['total_sales']:,.0f} CLP | Orders={res_today['orders']} | Ticket=${res_today['avg_ticket']:,.0f} | Discounts=${res_today['total_discounts']:,.0f}")

print("\n2. Fetching Last 7 Days (Oct 30 - Nov 6)...")
res_week = fetch_period("2026-10-30T03:00:00Z", "2026-11-06T04:00:00Z")
print(f"Week: Sales=${res_week['total_sales']:,.0f} CLP | Orders={res_week['orders']} | Ticket=${res_week['avg_ticket']:,.0f} | Discounts=${res_week['total_discounts']:,.0f}")

print("\n3. Fetching Previous Full Month (Oct 1 - Oct 31, 2026)...")
res_month = fetch_period("2026-10-01T03:00:00Z", "2026-11-01T03:00:00Z")
print(f"Last Month (Oct): Sales=${res_month['total_sales']:,.0f} CLP | Orders={res_month['orders']} | Ticket=${res_month['avg_ticket']:,.0f} | Discounts=${res_month['total_discounts']:,.0f}")

print("\n4. Fetching Same Month 3 Previous Years (October comparisons):")
for yr in [2025, 2024, 2023]:
    res_yr = fetch_period(f"{yr}-10-01T03:00:00Z", f"{yr}-11-01T03:00:00Z", include_discounts=False)
    print(f"October {yr}: Sales=${res_yr['total_sales']:,.0f} CLP | Orders={res_yr['orders']} | Ticket=${res_yr['avg_ticket']:,.0f}")

print("\n5. Fetching Same Month (November 1-5 MTD) across 2026, 2025, 2024, 2023:")
for yr in [2026, 2025, 2024, 2023]:
    res_nov = fetch_period(f"{yr}-11-01T03:00:00Z", f"{yr}-11-06T00:00:00Z", include_discounts=False)
    print(f"Nov 1-5 {yr}: Sales=${res_nov['total_sales']:,.0f} CLP | Orders={res_nov['orders']} | Ticket=${res_nov['avg_ticket']:,.0f}")
