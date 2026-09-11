with open('app.py', 'r') as f:
    lines = f.readlines()

block = lines[1360:1662]

for i, line in enumerate(block):
    if 'st.rerun' in line:
        # print context
        print(f"Index {i}: {line.strip()}")
        # print surrounding lines
        for j in range(max(0, i-3), min(len(block), i+3)):
            print(f"  {j}: {block[j].strip()}")
        print("-" * 20)
