with open("app.py") as f:
    for i, line in enumerate(f, 1):
        if "main_tab" in line:
            print(f"{i}: {line.strip()}")
