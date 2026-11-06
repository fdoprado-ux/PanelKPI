with open('openapi.yml', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect the first 200 lines of openapi.yml
lines = text.splitlines()
print("\n".join(lines[:120]))
