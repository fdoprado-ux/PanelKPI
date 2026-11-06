with open('openapi.yml', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [line for line in text.splitlines() if any(k in line.lower() for k in ['summary', 'stat', 'report']) and line.strip().startswith('/')]
print("Paths with summary/stat/report:")
for m in set(matches):
    print(m)
