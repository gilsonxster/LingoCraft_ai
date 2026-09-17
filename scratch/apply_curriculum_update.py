import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import build_all_extra as extra

with open("curriculum_data.py", "r", encoding="utf-8") as f:
    text = f.read()

# Marker 1: end of hacer PT (lines 388-391)
m1 = '                    "Qual é o melhor macete para memorizar \'hice, hiciste, hizo\'?"\n                ]\n            )\n        }'
r1 = f'''                    "Qual é o melhor macete para memorizar 'hice, hiciste, hizo'?"
                ]
            ){extra.HACER_PT_EXTRA}
        }})'''

# Marker 2: end of hacer EN (lines 677-680)
m2 = '                "Can you give me a trick or mnemonic to easily remember \'yo hice, tú hiciste, él hizo\'?"\n            ]\n        )\n    }'
r2 = f'''                "Can you give me a trick or mnemonic to easily remember 'yo hice, tú hiciste, él hizo'?"
            ]
        ){extra.HACER_EN_EXTRA}
    }})'''

# Marker 3: end of tener PT (lines 970-973)
m3 = '                    "Quais outros verbos usam o radical com -uv- (como estar -> estuve, andar -> anduve)?"\n                ]\n            )\n        }'
r3 = f'''                    "Quais outros verbos usam o radical com -uv- (como estar -> estuve, andar -> anduve)?"
                ]
            ){extra.TENER_PT_EXTRA}
        }})'''

# Marker 4: end of tener EN (lines 1259-1262)
m4 = '                "What other Spanish verbs share this -uv- preterite stem (like estar -> estuve, andar -> anduve)?"\n            ]\n        )\n    }'
r4 = f'''                "What other Spanish verbs share this -uv- preterite stem (like estar -> estuve, andar -> anduve)?"
            ]
        ){extra.TENER_EN_EXTRA}
    }})'''

# Check markers exist
for m, label in [(m1, "m1"), (m2, "m2"), (m3, "m3"), (m4, "m4")]:
    if m not in text:
        print(f"Error: Marker {label} not found in curriculum_data.py!")
        sys.exit(1)
    print(f"Marker {label} found.")

text = text.replace(m1, r1, 1)
text = text.replace(m2, r2, 1)
text = text.replace(m3, r3, 1)
text = text.replace(m4, r4, 1)

# Now replace the 4 "return {" with "return _add_pack_aliases({"
parts = text.split("return {")
print(f"Number of 'return {{' occurrences: {len(parts)-1}")
if len(parts) == 5:
    text = "return _add_pack_aliases({".join(parts)
    print("Replaced all 4 return statements with return _add_pack_aliases({")
else:
    print("Warning: expected 4 occurrences of 'return {', found", len(parts)-1)
    sys.exit(1)

# Update tenses_roadmap in SPANISH_HACER_CURRICULUM and SPANISH_TENER_CURRICULUM
old_roadmap = "tenses_roadmap=['Infinitivo', 'Gerundio', 'Participio', 'Presente de Indicativo', 'Pretérito Indefinido']"
new_roadmap = "tenses_roadmap=['Infinitivo', 'Gerundio', 'Participio', 'Presente de Indicativo', 'Pretérito Indefinido', 'Pretérito Imperfecto', 'Futuro Próximo', 'Futuro Simple', 'Condicional Simple', 'Presente de Subjuntivo']"

if old_roadmap in text:
    text = text.replace(old_roadmap, new_roadmap)
    print("Updated tenses_roadmap.")
else:
    print("Warning: old_roadmap not found!")
    sys.exit(1)

# Write to a test file first and verify syntax
with open("scratch/curriculum_data_test.py", "w", encoding="utf-8") as f:
    f.write(text)

print("scratch/curriculum_data_test.py written. Verifying compilation...")
import py_compile
py_compile.compile("scratch/curriculum_data_test.py", doraise=True)
print("Compiled successfully!")

# Now overwrite curriculum_data.py
with open("curriculum_data.py", "w", encoding="utf-8") as f:
    f.write(text)

print("curriculum_data.py updated and verified!")
