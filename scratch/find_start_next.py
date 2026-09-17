with open("app.py") as f:
    for i, line in enumerate(f, 1):
        if "start_next_curriculum_topic" in line:
            print(f"{i}: {line.strip()}")
