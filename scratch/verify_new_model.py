import os

keywords = ['gemini-3.1-flash-lite']
found = False

for root, dirs, files in os.walk('.'):
    if '.venv' in dirs:
        dirs.remove('.venv')
    if '.git' in dirs:
        dirs.remove('.git')
    for file in files:
        if file.endswith('.py'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
                for kw in keywords:
                    if kw in content:
                        print(f"Found '{kw}' in {filepath}")
                        found = True

if not found:
    print("No occurrences of gemini-3.1-flash-lite found.")
