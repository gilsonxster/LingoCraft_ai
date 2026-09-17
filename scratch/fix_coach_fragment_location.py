with open("app.py", "r") as f:
    code = f.read()

# Locate _coach_tab_chat_fragment
frag_start_marker = "@st.fragment\ndef _coach_tab_chat_fragment(curr_tense_name: str, coach_prompts: list):"
frag_end_marker = "elif selected_tab == MAIN_TAB_COACH:"

start_idx = code.find(frag_start_marker)
end_idx = code.find(frag_end_marker)
assert start_idx != -1 and end_idx != -1, "Could not find fragment boundaries"

fragment_code = code[start_idx:end_idx].strip()

# Remove fragment from between if and elif
code = code[:start_idx] + code[end_idx:]

# Insert fragment before if "_pending_main_tab"
insert_marker = 'if "_pending_main_tab" in st.session_state:'
insert_idx = code.find(insert_marker)
assert insert_idx != -1, "Could not find insert_marker"

code = code[:insert_idx] + fragment_code + "\n\n\n" + code[insert_idx:]

with open("app.py", "w") as f:
    f.write(code)

print("Fragment moved successfully!")
