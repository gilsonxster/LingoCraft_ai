import re

with open("app.py", "r") as f:
    code = f.read()

# 1. Soften dropdown borders in CSS
css_search = "/* Disable tooltip popups in sidebar"
css_addition = """    /* Soften dropdown border radius */
    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
    }
    .card-surface {
        max-width: 860px;
        margin: 0 auto;
    }
    """ + css_search

assert css_search in code, "Could not find css_search in app.py"
code = code.replace(css_search, css_addition, 1)

# 2. Update render_incontext_coach
coach_old = '''def render_incontext_coach(current_tense_name: str, step_num: int, pack, target_l: str, native_l: str):
    """
    Renders an in-context Coach consultation widget directly inside the active flashcard container
    so learners can resolve doubts immediately without losing their card step or study flow.
    Uses @st.fragment so questions are sent to the backend without refreshing the entire page.
    """
    step_ans_key = f"incontext_ans_{current_tense_name}_{step_num}"
    with st.popover(f"💬 Ask Coach about {current_tense_name}", use_container_width=False):
        st.markdown(f"<div style='font-size: 0.875rem; color: #5F6368; margin-bottom: 8px;'>Got a question about <strong>{current_tense_name}</strong>? Ask here and continue your study flow without losing your card.</div>", unsafe_allow_html=True)
        prompts = getattr(pack, "suggested_coach_prompts", []) if pack else []
        _incontext_coach_fragment(current_tense_name, step_num, prompts, target_l, native_l)'''

coach_new = '''def render_incontext_coach(current_tense_name: str, step_num: int, pack, target_l: str, native_l: str):
    """
    Renders an in-context Coach consultation popover at the top-right of the active flashcard container
    so learners can resolve doubts immediately without losing their card step or pushing down navigation.
    Uses @st.fragment so questions are sent to the backend without refreshing the entire page.
    """
    with st.popover(f"💬 Ask Coach", use_container_width=True, help=f"Ask Coach LingoCraft about {current_tense_name}"):
        st.markdown(f"<div style='font-size: 0.875rem; color: #5F6368; margin-bottom: 8px;'>Got a question about <strong>{current_tense_name}</strong>? Ask Coach LingoCraft and resume studying seamlessly.</div>", unsafe_allow_html=True)
        prompts = getattr(pack, "suggested_coach_prompts", []) if pack else []
        _incontext_coach_fragment(current_tense_name, step_num, prompts, target_l, native_l)'''

assert coach_old in code, "Could not find coach_old in app.py"
code = code.replace(coach_old, coach_new, 1)

print("Step 1 & 2 applied successfully")
