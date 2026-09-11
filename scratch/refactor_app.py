with open('app.py', 'r') as f:
    lines = f.readlines()

# Extract block (lines 1361-1662, 1-indexed -> 0-indexed: 1360 to 1661 inclusive)
block = lines[1360:1662]

# Modify reruns in block
indices_to_fragment = [13, 43, 83, 89, 129, 136, 161, 169, 301]
indices_to_app = [227, 251, 291]

for idx in indices_to_fragment:
    block[idx] = block[idx].replace('st.rerun()', 'st.rerun(scope="fragment")')

for idx in indices_to_app:
    block[idx] = block[idx].replace('st.rerun()', 'st.rerun(scope="app")')

# Remove block from lines
del lines[1360:1662]

# Insert call to fragment at line 1360
call_fragment = "        _flashcard_study_fragment(pack, current_tense_name, total_tenses)\n"
lines.insert(1360, call_fragment)

# Define fragment
indented_block = ["    " + line for line in block]
fragment_def = [
    "@st.fragment\n",
    "def _flashcard_study_fragment(pack, current_tense_name: str, total_tenses: int):\n",
    "    \"\"\"\n",
    "    Isolated Streamlit fragment for flashcard study (stepper and card content).\n",
    "    Interactions here execute in-place without triggering a full page rerun by default.\n",
    "    \"\"\"\n",
    "    step_names = [\n",
    "        \"1. Concept & rule\",\n",
    "        \"2. Bilingual example\",\n",
    "        \"3. Pronunciation guide\",\n",
    "        \"4. Speech validation\",\n",
    "        \"5. Conjugation quiz\"\n",
    "    ]\n"
]

fragment_full = fragment_def + indented_block

# Insert fragment at line 585 (0-indexed 584)
# We do this last so we don't mess up the 1360 index before we use it.
for i, line in enumerate(fragment_full):
    lines.insert(584 + i, line)

# Write back to app.py
with open('app.py', 'w') as f:
    f.writelines(lines)

print("Refactoring complete!")
