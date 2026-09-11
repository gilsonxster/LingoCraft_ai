import re

with open('app.py', 'r') as f:
    content = f.read()

matches = [m.start() for m in re.finditer('target_l', content)]
for match in matches:
    # get line number
    line_no = content[:match].count('\n') + 1
    print(f"Found at line {line_no}")
