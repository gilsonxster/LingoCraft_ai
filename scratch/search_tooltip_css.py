with open("app.py") as f:
    for i, line in enumerate(f, 1):
        if "tooltip" in line.lower() or "popover" in line.lower() or "title=" in line.lower():
            print(f"{i}: {line.strip()}")
