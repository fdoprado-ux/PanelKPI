import urllib.request, json, ssl
ctx = ssl.create_default_context()
token = 'eyJhbGciOiJIUzI1NiJ9.eyJhaSI6NDU1MjMsInVpIjoxMjMsInBhIjp0cnVlLCJleHAiOjE3OTQwMjIyNTl9.mDENiJabHYf2iSW2UsVeN0Csy-RfMiu4f7QcTuk3D3w'
headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}

# 1. First, fetch categories and classify them
req_c = urllib.request.Request("https://api.fu.do/v1alpha1/product-categories?page[size]=100", headers=headers)
with urllib.request.urlopen(req_c, context=ctx) as r:
    cats = json.loads(r.read().decode('utf-8'))['data']

bar_category_ids = set()
for c in cats:
    name_l = c['attributes']['name'].lower()
    if any(k in name_l for k in ['cerveza', 'coctel', 'pisco', 'vodka', 'whisky', 'ron', 'vino', 'tequila', 'gin', 'licor', 'bebida', 'sin alcohol', 'cafeteria', 'por copa', 'shots', 'liquidos', 'carmenere', 'merlot', 'cabernet', 'moonshine', 'sun drinks']):
        bar_category_ids.add(c['id'])

# 2. Fetch products and map to category
products_map = {}
page = 1
while True:
    req_p = urllib.request.Request(f"https://api.fu.do/v1alpha1/products?page[size]=100&page[number]={page}", headers=headers)
    with urllib.request.urlopen(req_p, context=ctx) as r:
        p_res = json.loads(r.read().decode('utf-8'))['data']
        for p in p_res:
            cat_id = p.get('relationships', {}).get('productCategory', {}).get('data', {}).get('id')
            is_bar = cat_id in bar_category_ids
            products_map[p['id']] = {
                'name': p['attributes']['name'],
                'price': p['attributes'].get('price', 0),
                'categoryId': cat_id,
                'isBar': is_bar
            }
        if len(p_res) < 100: break
        page += 1

print(f"Total products mapped: {len(products_map)}")

# 3. Fetch recent items from Oct 1 to Nov 6 (or last 2,000 items) to rank them
food_ranking = {}
bar_ranking = {}

page = 1
for page in range(1, 15): # sample 7,000 items
    req_i = urllib.request.Request(f"https://api.fu.do/v1alpha1/items?page[size]=500&page[number]={page}&sort=-id", headers=headers)
    with urllib.request.urlopen(req_i, context=ctx) as r:
        i_res = json.loads(r.read().decode('utf-8'))['data']
        for it in i_res:
            attrs = it['attributes']
            if attrs.get('canceled'): continue
            p_id = it.get('relationships', {}).get('product', {}).get('data', {}).get('id')
            if not p_id or p_id not in products_map: continue
            
            prod = products_map[p_id]
            qty = attrs.get('quantity', 1) or 1
            revenue = (attrs.get('price', 0) or 0) * qty

            target = bar_ranking if prod['isBar'] else food_ranking
            p_name = prod['name']
            if p_name.startswith('↑↑↑'): continue # exclude modifiers/mixers

            if p_name not in target:
                target[p_name] = {'units': 0, 'revenue': 0, 'price': prod['price']}
            target[p_name]['units'] += qty
            target[p_name]['revenue'] += revenue

top_food = sorted(food_ranking.items(), key=lambda x: x[1]['units'], reverse=True)[:8]
top_bar = sorted(bar_ranking.items(), key=lambda x: x[1]['units'], reverse=True)[:8]

print("\n=== TOP PLATOS (COMIDA) ===")
for name, data in top_food:
    print(f"{name:30} | Units: {data['units']:4} | Revenue: ${data['revenue']:,.0f} CLP")

print("\n=== TOP LICORES / BAR (BEBIDAS) ===")
for name, data in top_bar:
    print(f"{name:30} | Units: {data['units']:4} | Revenue: ${data['revenue']:,.0f} CLP")
