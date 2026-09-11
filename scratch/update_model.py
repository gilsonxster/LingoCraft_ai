import os

files_to_update = [
    'skills/coach_chat_agent.py',
    'skills/speech_agent.py',
    'skills/curriculum_agent.py',
    'skills/flashcard_agent.py',
    'skills/quiz_agent.py'
]

for filepath in files_to_update:
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read()
        
        new_content = content.replace('gemini-2.5-flash', 'gemini-3.1-flash-lite')
        
        with open(filepath, 'w') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
    else:
        print(f"File not found: {filepath}")

print("All requested files updated.")
