with open("app.py") as f:
    in_sidebar = False
    for i, line in enumerate(f, 1):
        if "with st.sidebar" in line:
            in_sidebar = True
        if in_sidebar and line.startswith("# Main Area Layout"):
            in_sidebar = False
        if in_sidebar and "help=" in line:
            print(f"{i}: {line.strip()}")
