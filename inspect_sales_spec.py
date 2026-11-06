with open('openapi.yml', 'r', encoding='utf-8') as f:
    text = f.read()

def print_section(title, start_str, length=3000):
    idx = text.find(start_str)
    if idx != -1:
        print(f"=== {title} ===")
        print(text[idx:idx+length])
    else:
        print(f"=== {title} NOT FOUND ===")

print_section("/sales GET", "  /sales:\n    get:")
print_section("/discounts GET", "  /discounts:\n    get:")
