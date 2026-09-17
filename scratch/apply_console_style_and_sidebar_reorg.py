import re

with open("app.py", "r") as f:
    content = f.read()

# 1. Add Google Cloud Console CSS styling to the <style> block
old_css_anchor = """    /* Disable tooltip popups in sidebar to prevent blocking button interactions */
    [data-testid="stSidebar"] [data-testid="stTooltipContent"],
    [data-testid="stSidebar"] [data-testid="stTooltipHoverTarget"] + div,
    [data-testid="stSidebar"] div[role="tooltip"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }
</style>"""

new_css = """    /* Disable tooltip popups in sidebar to prevent blocking button interactions */
    [data-testid="stSidebar"] [data-testid="stTooltipContent"],
    [data-testid="stSidebar"] [data-testid="stTooltipHoverTarget"] + div,
    [data-testid="stSidebar"] div[role="tooltip"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }

    /* Google Cloud Console Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #F0F5FE !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: #DDE5F2 !important;
    }

    /* Google Cloud Console Roadmap Navigation Item Styling */
    [data-testid="stSidebar"] div[class*="st-key-sidebar_tense_"] {
        margin: 2px 0 !important;
    }

    [data-testid="stSidebar"] div[class*="st-key-sidebar_tense_"] > button {
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        text-align: left !important;
        width: 100% !important;
        padding: 8px 12px !important;
        min-height: 42px !important;
        border-radius: 6px !important;
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        transition: background-color 0.15s ease, color 0.15s ease !important;
    }

    [data-testid="stSidebar"] div[class*="st-key-sidebar_tense_"] > button div[data-testid="stMarkdownContainer"] {
        text-align: left !important;
        width: 100% !important;
        display: flex !important;
        justify-content: flex-start !important;
    }

    [data-testid="stSidebar"] div[class*="st-key-sidebar_tense_"] > button div[data-testid="stMarkdownContainer"] p {
        text-align: left !important;
        font-size: 0.88rem !important;
        letter-spacing: -0.01rem !important;
        margin: 0 !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
    }

    /* Inactive Roadmap Item - Clean, Flat, Borderless */
    [data-testid="stSidebar"] div[class*="st-key-sidebar_tense_"] > button[kind="secondary"] {
        background-color: transparent !important;
        color: #1B2E5D !important;
        border: 1px solid transparent !important;
    }

    [data-testid="stSidebar"] div[class*="st-key-sidebar_tense_"] > button[kind="secondary"] p {
        color: #1B2E5D !important;
        font-weight: 500 !important;
    }

    [data-testid="stSidebar"] div[class*="st-key-sidebar_tense_"] > button[kind="secondary"]:hover {
        background-color: #E4EBF7 !important;
        color: #1B2E5D !important;
    }

    /* Active Roadmap Item - Google Cloud Console Selected Row Highlight (#E9EEF7) */
    [data-testid="stSidebar"] div[class*="st-key-sidebar_tense_"] > button[kind="primary"] {
        background-color: #E9EEF7 !important;
        color: #1B2E5D !important;
        border: 1px solid #D7E1EE !important;
        box-shadow: 0 1px 2px rgba(27, 46, 93, 0.04) !important;
    }

    [data-testid="stSidebar"] div[class*="st-key-sidebar_tense_"] > button[kind="primary"] p {
        color: #1B2E5D !important;
        font-weight: 600 !important;
    }

    [data-testid="stSidebar"] div[class*="st-key-sidebar_tense_"] > button[kind="primary"]:hover {
        background-color: #E0E8F4 !important;
    }

    [data-testid="stSidebar"] div[class*="st-key-sidebar_tense_"] > button:focus:not(:focus-visible) {
        outline: none !important;
        box-shadow: none !important;
    }
</style>"""

assert old_css_anchor in content, "old_css_anchor not found!"
content = content.replace(old_css_anchor, new_css, 1)

# 2. Add helper function get_tense_nav_icon before select_tense_and_study
helper_anchor = """def select_tense_and_study(idx: int):"""
helper_code = """def get_tense_nav_icon(tense_name: str, idx: int, is_comp: bool, is_rev: bool, is_act: bool) -> str:
    \"\"\"Returns a Google Cloud Console style icon representing stage category or completion state.\"\"\"
    if is_rev:
        return "🔄"
    if is_comp:
        return "✓"
    t_lower = tense_name.lower()
    if "subjunt" in t_lower:
        return "🎭"
    if "imperativ" in t_lower:
        return "📢"
    if "condicion" in t_lower or "would" in t_lower:
        return "💡"
    if "próximo" in t_lower or "proximo" in t_lower or "going to" in t_lower:
        return "➡️"
    if "futur" in t_lower:
        return "🔮"
    if "imperfect" in t_lower or "imperfeito" in t_lower:
        return "🕰️"
    if "indefinid" in t_lower or "perfeito" in t_lower:
        return "⏪"
    if "present" in t_lower:
        return "💬"
    if "infinitiv" in t_lower:
        return "📋"
    if "gerund" in t_lower:
        return "⚡"
    if "particip" in t_lower:
        return "📌"
    return "🔹"


def select_tense_and_study(idx: int):"""

assert helper_anchor in content, "helper_anchor not found!"
content = content.replace(helper_anchor, helper_code, 1)

# 3. Update Switch Topic / Language popover caption
old_caption = 'st.caption("ℹ️ *Enter a Gemini API Key under Settings below to generate custom AI topics.*")'
new_caption = 'st.caption("ℹ️ *Enter a Gemini API Key on the sidebar below to generate custom AI topics.*")'
assert old_caption in content, "old_caption not found!"
content = content.replace(old_caption, new_caption, 1)

# 4. Insert API Key input directly below Switch Topic / Language popover
old_switcher_end = """                    st.success("Roadmap successfully initialized!")
                    st.rerun()

    st.markdown("<hr style='margin: 10px 0 12px 0;'>", unsafe_allow_html=True)"""

new_switcher_end = """                    st.success("Roadmap successfully initialized!")
                    st.rerun()

    # Gemini API Key Input (Positioned directly below Switch Topic/Language)
    api_key_input = st.text_input(
        "🔑 Gemini API Key (Optional):",
        value=st.session_state.api_key,
        type="password",
        placeholder="AIzaSy...",
        help="Leave blank to use pre-loaded curated curriculum (100% offline), or enter your Gemini API key for dynamic AI topics.",
        key="sidebar_gemini_api_key"
    )
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        orchestrator = LingoCraftOrchestrator(api_key=api_key_input)
        st.rerun()

    st.markdown("<hr style='margin: 10px 0 12px 0;'>", unsafe_allow_html=True)"""

assert old_switcher_end in content, "old_switcher_end not found!"
content = content.replace(old_switcher_end, new_switcher_end, 1)

# 5. Update roadmap header and buttons to console navigation style
old_roadmap = """    st.markdown(f\"\"\"
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px;">
        <span style="font-weight: 700; color: #202124; font-size: 0.95rem;">🗺️ Roadmap</span>
        <span style="font-size: 0.78rem; color: #5F6368; font-weight: 600;">{comp_count}/{total_tenses} Complete</span>
    </div>
    \"\"\", unsafe_allow_html=True)
    st.progress(comp_count / max(total_tenses, 1))

    needs_rev_set = st.session_state.get("needs_review_tenses", set())
    for idx, tense in enumerate(roadmap):
        is_act = (idx == st.session_state.active_tense_index)
        is_comp = (idx in st.session_state.completed_tenses)
        is_rev = (idx in needs_rev_set)

        if is_act:
            label = f"● {idx+1}. {tense}"
            btn_t = "primary"
        elif is_comp:
            label = f"✓ {idx+1}. {tense}"
            btn_t = "secondary"
        elif is_rev:
            label = f"🔄 {idx+1}. {tense}"
            btn_t = "secondary"
        else:
            label = f"⏳ {idx+1}. {tense}"
            btn_t = "secondary"

        st.button(
            label,
            key=f"sidebar_tense_{idx}",
            use_container_width=True,
            type=btn_t,
            on_click=select_tense_and_study,
            args=(idx,)
        )"""

new_roadmap = """    st.markdown(f\"\"\"
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px; padding: 0 2px;">
        <span style="font-weight: 600; color: #1B2E5D; font-size: 0.92rem; letter-spacing: -0.01rem;">Roadmap Stages</span>
        <span style="font-size: 0.78rem; color: #545F72; font-weight: 600;">{comp_count}/{total_tenses} Complete</span>
    </div>
    \"\"\", unsafe_allow_html=True)
    st.progress(comp_count / max(total_tenses, 1))

    needs_rev_set = st.session_state.get("needs_review_tenses", set())
    for idx, tense in enumerate(roadmap):
        is_act = (idx == st.session_state.active_tense_index)
        is_comp = (idx in st.session_state.completed_tenses)
        is_rev = (idx in needs_rev_set)

        nav_icon = get_tense_nav_icon(tense, idx, is_comp, is_rev, is_act)
        label = f"{nav_icon}   {idx+1}. {tense}"
        btn_t = "primary" if is_act else "secondary"

        st.button(
            label,
            key=f"sidebar_tense_{idx}",
            use_container_width=True,
            type=btn_t,
            on_click=select_tense_and_study,
            args=(idx,)
        )"""

assert old_roadmap in content, "old_roadmap not found!"
content = content.replace(old_roadmap, new_roadmap, 1)

# 6. Remove duplicate API key from Settings & Sessions
old_settings_key = """        st.markdown("---")
        # API Key management
        key_input = st.text_input(
            "Gemini API Key (Optional)",
            value=st.session_state.api_key,
            type="password",
            help="Leave blank to use pre-loaded curated curriculum or enter your key for full dynamic AI generation."
        )
        if key_input != st.session_state.api_key:
            st.session_state.api_key = key_input
            orchestrator = LingoCraftOrchestrator(api_key=key_input)
            st.rerun()

        st.caption("ℹ️ *Required only for custom AI topics; curated topics work 100% offline without a key.*")"""

assert old_settings_key in content, "old_settings_key not found!"
content = content.replace(old_settings_key, "", 1)

# 7. Add "About" popover to the bottom of the sidebar
old_sidebar_end = """            if st.button("Clear telemetry logs", key="clear_telemetry_btn", use_container_width=True):
                st.session_state.ve_logs = []
                st.rerun()"""

new_sidebar_end = """            if st.button("Clear telemetry logs", key="clear_telemetry_btn", use_container_width=True):
                st.session_state.ve_logs = []
                st.rerun()

    with st.popover("ℹ️ About LingoCraft", use_container_width=True, help="About LingoCraft AI"):
        st.markdown("#### 🎓 LingoCraft AI")
        st.markdown(\"\"\"
        **Empathetic Active Recall Foreign Language Coach**

        **5-Stage Pedagogical Flow:**
        1. **Rule & Base Concept**
        2. **Bilingual Comparative Phrase**
        3. **Phonetic Breakdown & Audio**
        4. **Voice Practice & Validation**
        5. **Conjugation Quiz Challenge**

        *Craftsman Gamification with persistent XP & spaced repetition.*
        \"\"\")
        st.caption(f"Active Session: `{st.session_state.session_id}`")"""

assert old_sidebar_end in content, "old_sidebar_end not found!"
content = content.replace(old_sidebar_end, new_sidebar_end, 1)

# 8. Clean up col_hdr_xp in main header to remove "About" from main page and display full XP badge
old_col_hdr_xp = """with col_hdr_xp:
    xp_val = st.session_state.get("xp_points", 0)
    col_badge, col_info = st.columns([3.4, 0.8], vertical_alignment="center")
    with col_badge:
        st.markdown(f\"\"\"
        <div style="background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 12px; padding: 4px 10px; box-shadow: 0 1px 2px rgba(60,64,67,0.04); display: flex; flex-direction: column; align-items: flex-end;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span style="font-weight: 700; color: #174EA6; font-size: 0.92rem;">⚡ {xp_val} XP</span>
                <span class="badge-active" style="font-size: 0.72rem; padding: 2px 7px;">{rank_info['icon']} Lvl {rank_info['level']}: {rank_info['name']}</span>
            </div>
            <div style="font-size: 0.68rem; color: #5F6368; margin-top: 1px;">
                {rank_info['current_xp']} / {rank_info['next_level_xp']} XP ({int(rank_info['progress_ratio'] * 100)}%)
            </div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with col_info:
        with st.popover("About", use_container_width=True, help="About LingoCraft AI"):
            st.markdown("#### 🎓 LingoCraft AI")
            st.markdown(\"\"\"
            **Empathetic Active Recall Foreign Language Coach**

            5-Stage Pedagogical Flow:
            1. **Rule & Base Concept**
            2. **Bilingual Comparative Phrase**
            3. **Phonetic Breakdown & Audio**
            4. **Voice Practice & Validation**
            5. **Conjugation Quiz Challenge**

            *Craftsman Gamification with persistent XP & spaced repetition.*
            \"\"\")
            st.caption(f"Session: `{st.session_state.session_id}`")"""

new_col_hdr_xp = """with col_hdr_xp:
    xp_val = st.session_state.get("xp_points", 0)
    st.markdown(f\"\"\"
    <div style="background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 12px; padding: 4px 12px; box-shadow: 0 1px 2px rgba(60,64,67,0.04); display: flex; flex-direction: column; align-items: flex-end;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-weight: 700; color: #174EA6; font-size: 0.95rem;">⚡ {xp_val} XP</span>
            <span class="badge-active" style="font-size: 0.75rem; padding: 2px 8px;">{rank_info['icon']} Lvl {rank_info['level']}: {rank_info['name']}</span>
        </div>
        <div style="font-size: 0.7rem; color: #5F6368; margin-top: 2px;">
            {rank_info['current_xp']} / {rank_info['next_level_xp']} XP ({int(rank_info['progress_ratio'] * 100)}%)
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)"""

assert old_col_hdr_xp in content, "old_col_hdr_xp not found!"
content = content.replace(old_col_hdr_xp, new_col_hdr_xp, 1)

with open("app.py", "w") as f:
    f.write(content)

print("app.py successfully updated with Google Cloud Console navigation and reorganized sidebar!")
