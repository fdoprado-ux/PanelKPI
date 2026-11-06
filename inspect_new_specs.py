with open('openapi.yml', 'r', encoding='utf-8') as f:
    text = f.read()

def print_op(path):
    idx = text.find(path)
    if idx != -1:
        print(f"=== {path} ===")
        print(text[idx:idx+2500])

print_op("/cash-movements:")
print_op("/payments:")
