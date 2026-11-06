with open('openapi.yml', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [line for line in text.splitlines() if 'cash' in line.lower() and line.strip().startswith('/')]
print("Paths with cash:")
for m in set(matches):
    print(m)
