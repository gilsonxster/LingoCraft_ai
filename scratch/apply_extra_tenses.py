import re
import sys

with open("curriculum_data.py", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add _add_pack_aliases before build_spanish_hacer_pack
alias_func = '''def _add_pack_aliases(packs: Dict[str, TenseFlashcardPack]) -> Dict[str, TenseFlashcardPack]:
    """Expands tense pack dictionary with common canonical aliases."""
    alias_map = {
        'Condicional Simple': ['Condicional', 'Condicional Simple de Indicativo', 'Condicional de Indicativo'],
        'Pretérito Imperfecto': ['Pretérito Imperfecto de Indicativo', 'Imperfecto', 'Copretérito'],
        'Futuro Simple': ['Futuro', 'Futuro Simple de Indicativo'],
        'Futuro Próximo': ['Futuro Inmediato', 'Ir a + Infinitivo', 'Futuro Proximo'],
        'Presente de Subjuntivo': ['Presente Subjuntivo', 'Subjuntivo'],
        'Presente de Indicativo': ['Presente', 'Presente Indicativo'],
        'Pretérito Indefinido': ['Pretérito', 'Pretérito Indefinido de Indicativo', 'Indefinido', 'Pasado Simple']
    }
    result = dict(packs)
    for canonical_name, aliases in alias_map.items():
        if canonical_name in packs:
            for al in aliases:
                if al not in result:
                    result[al] = packs[canonical_name]
    return result

'''

if "def _add_pack_aliases" not in content:
    content = content.replace("def build_spanish_hacer_pack", alias_func + "def build_spanish_hacer_pack", 1)

print("Step 1 done. Alias function added.")
with open("curriculum_data.py", "w", encoding="utf-8") as f:
    f.write(content)
