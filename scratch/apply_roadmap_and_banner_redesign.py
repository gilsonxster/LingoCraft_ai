with open("app.py", "r") as f:
    code = f.read()

# 1. Fix module docstring at top
old_top = '''from streamlit.errors import StreamlitWidgetAlreadyInstantiatedError
"""
LingoCraft AI - Streamlit Application.
Interactive, empathetic, tense-by-tense language learning coach with 5-stage flashcard system.
"""
import streamlit as st'''

new_top = '''"""
LingoCraft AI Application.
Interactive, empathetic, tense-by-tense language learning coach with 5-stage flashcard system.
"""
from streamlit.errors import StreamlitWidgetAlreadyInstantiatedError
import streamlit as st'''

assert old_top in code, "Could not find old_top in app.py"
code = code.replace(old_top, new_top, 1)

# 2. Extract entire sidebar content to restructure
sidebar_marker = "with st.sidebar:"
assert sidebar_marker in code, "Could not find with st.sidebar:"

old_sidebar_code = code[code.find(sidebar_marker):code.find("# Display session loaded notification toast if set")]

new_sidebar_code = """with st.sidebar:
    # 1. Top Branding & Active Topic Anchor
    st.markdown('<div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;"><span style="font-size:1.6rem;">🎓</span><span style="font-size:1.35rem; font-weight:700; color:#174EA6; letter-spacing:-0.02rem;">LingoCraft</span></div>', unsafe_allow_html=True)

    cur_topic = st.session_state.current_curriculum.get("topic", "Spanish: Verbo 'Hacer'")
    target_l = st.session_state.current_curriculum.get("target_language", "Spanish")
    native_l = st.session_state.current_curriculum.get("native_language", "English")
    flag_emoji = "🇪🇸" if "span" in target_l.lower() else ("🇧🇷" if "portug" in target_l.lower() else "🇬🇧")

    st.markdown(f\"\"\"
    <div style="background: #F8F9FA; border: 1px solid #DADCE0; border-radius: 10px; padding: 6px 12px; margin: 4px 0 10px 0;">
        <div style="font-size: 0.68rem; font-weight: 700; color: #5F6368; text-transform: uppercase; letter-spacing: 0.04rem;">Active Course</div>
        <div style="font-size: 0.88rem; font-weight: 600; color: #174EA6; margin-top: 1px;">{flag_emoji} {cur_topic}</div>
    </div>
    \"\"\", unsafe_allow_html=True)

    # Topic Initializer & Switcher Popover
    with st.popover("📚 Switch Topic / Language", use_container_width=True):
        st.markdown("##### Choose Curriculum Topic")
        study_mode = st.segmented_control(
            "Select Curriculum Mode:",
            ["Curated Core Topics", "Custom Topic (AI Powered)"],
            default="Curated Core Topics",
            label_visibility="collapsed"
        )
        if not study_mode:
            study_mode = "Curated Core Topics"

        if study_mode == "Curated Core Topics":
            curated_choices = [
                "Spanish: Irregular Verbs — Verbo 'Hacer'",
                "Spanish: 'Ser' vs 'Estar' (Essentials)",
                "Portuguese: Verbo Irregular — 'Fazer'",
                "Portuguese: Pretérito Perfeito vs Imperfeito",
                "English: Irregular Verbs — 'To Do / To Make'",
                "Spanish: Pretérito Indefinido vs Imperfecto"
            ]
            chosen_topic = st.selectbox("Choose a Curated Topic:", curated_choices)
            curated_native = st.selectbox("Your Native / Support Language:", ["English", "Portuguese", "Spanish"])

            if st.button("Load Selected Curriculum", use_container_width=True, type="primary"):
                if "Hacer" in chosen_topic or "Spanish" in chosen_topic:
                    curriculum_obj = get_curriculum_or_fallback(chosen_topic, "Spanish", curated_native)
                    st.session_state.current_curriculum = {
                        "topic": curriculum_obj.title,
                        "target_language": curriculum_obj.target_language,
                        "target_language_code": curriculum_obj.target_language_code,
                        "native_language": curriculum_obj.native_language,
                        "description": curriculum_obj.description,
                        "tenses_roadmap": curriculum_obj.tenses_roadmap,
                    }
                else:
                    target_l_sub = chosen_topic.split(":")[0].strip()
                    plan = orchestrator.initialize_curriculum(chosen_topic, target_l_sub, curated_native)
                    st.session_state.current_curriculum = plan

                st.session_state.active_tense_index = 0
                st.session_state.active_card_step = 1
                st.session_state.completed_card_steps = set()
                st.session_state.current_pack = None
                st.session_state.pack_cache = {}
                st.session_state.completed_tenses = set()
                st.session_state.needs_review_tenses = set()
                st.session_state.speech_eval_result = None
                st.session_state.quiz_eval_result = None
                safe_set_main_tab(MAIN_TAB_LEARN)
                auto_save_current_session()
                st.rerun()

        else:
            custom_target = st.selectbox("Target Language:", ["Spanish", "Portuguese", "English"])
            custom_native = st.selectbox("Native / Support Language:", ["English", "Portuguese", "Spanish"])
            custom_topic_text = st.text_input("Topic Description:", "Irregular Verbs: Verbo 'Tener'")
            if not st.session_state.api_key:
                st.caption("ℹ️ *Enter a Gemini API Key under Settings below to generate custom AI topics.*")

            if st.button("🚀 Initialize Custom Curriculum", use_container_width=True, type="primary"):
                with st.spinner("Initializing Curriculum Roadmap with LingoCraft AI..."):
                    plan = orchestrator.initialize_curriculum(custom_topic_text, custom_target, custom_native)
                    st.session_state.current_curriculum = plan
                    st.session_state.active_tense_index = 0
                    st.session_state.active_card_step = 1
                    st.session_state.completed_card_steps = set()
                    st.session_state.current_pack = None
                    st.session_state.pack_cache = {}
                    st.session_state.completed_tenses = set()
                    st.session_state.needs_review_tenses = set()
                    st.session_state.speech_eval_result = None
                    st.session_state.quiz_eval_result = None
                    safe_set_main_tab(MAIN_TAB_LEARN)
                    auto_save_current_session()
                    st.success("Roadmap successfully initialized!")
                    st.rerun()

    st.markdown("<hr style='margin: 10px 0 12px 0;'>", unsafe_allow_html=True)

    # 2. Pedagogical Roadmap (Top Priority - Immediately visible without scrolling)
    roadmap = st.session_state.current_curriculum.get("tenses_roadmap", [])
    total_tenses = len(roadmap)
    comp_count = len(st.session_state.completed_tenses)
    is_curriculum_completed = (
        total_tenses > 0 and (
            st.session_state.active_tense_index >= total_tenses
            or comp_count >= total_tenses
        )
    )

    if roadmap:
        if 0 <= st.session_state.active_tense_index < total_tenses:
            active_tense_name = roadmap[st.session_state.active_tense_index]
        else:
            active_tense_name = roadmap[-1]
    else:
        active_tense_name = "General"

    st.markdown(f\"\"\"
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
        )

    if is_curriculum_completed:
        st.success("🎉 Roadmap Mastered! Check the main screen to start your next recommended topic.")

    st.markdown("<hr style='margin: 14px 0 10px 0;'>", unsafe_allow_html=True)

    # 3. Settings & Sessions (Collapsed Accordion at the bottom)
    with st.expander("⚙️ Settings & Sessions", expanded=False):
        st.markdown(f"**Session Code:** `{st.session_state.session_id}`")
        st.caption("✅ Auto-saving active. Your progress is saved as you study.")

        col_new_s, col_save_s = st.columns(2)
        with col_new_s:
            if st.button("➕ New Session", help="Start fresh with a new session code", use_container_width=True):
                new_sid = session_manager.generate_session_id()
                st.session_state.session_id = new_sid
                st.query_params["sid"] = new_sid
                st.session_state.active_tense_index = 0
                st.session_state.active_card_step = 1
                st.session_state.completed_card_steps = set()
                st.session_state.completed_tenses = set()
                st.session_state.needs_review_tenses = set()
                st.session_state.xp_points = 0
                st.session_state.awarded_xp_events = set()
                st.session_state.current_pack = None
                st.session_state.pack_cache = {}
                st.session_state.speech_eval_result = None
                st.session_state.quiz_eval_result = None
                safe_set_main_tab(MAIN_TAB_LEARN)
                auto_save_current_session()
                st.rerun()
        with col_save_s:
            if st.button("💾 Save State", use_container_width=True):
                auto_save_current_session()
                st.toast("Progress saved to database!", icon="💾")

        st.markdown("---")
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

        st.caption("ℹ️ *Required only for custom AI topics; curated topics work 100% offline without a key.*")

        st.markdown("---")
        code_to_load = st.text_input("Resume by Session Code:", placeholder="e.g. lingo-123456", key="load_sid_input")
        if st.button("Load Session", use_container_width=True):
            if code_to_load.strip():
                loaded = session_manager.load_session(code_to_load.strip())
                if loaded:
                    st.session_state.session_id = code_to_load.strip()
                    st.query_params["sid"] = code_to_load.strip()
                    st.session_state.current_curriculum = loaded["current_curriculum"]
                    st.session_state.active_tense_index = loaded["active_tense_index"]
                    st.session_state.active_card_step = loaded["active_card_step"]
                    st.session_state.completed_tenses = set(loaded["completed_tenses"])
                    st.session_state.needs_review_tenses = set(loaded.get("needs_review_tenses", []))
                    st.session_state.completed_card_steps = set(loaded["completed_card_steps"])
                    st.session_state.chat_history = loaded["chat_history"]
                    st.session_state.xp_points = loaded.get("xp_points", 0)
                    st.session_state.awarded_xp_events = set()
                    st.session_state.current_pack = None
                    st.session_state.pack_cache = {}
                    st.session_state.speech_eval_result = None
                    st.session_state.quiz_eval_result = None
                    safe_set_main_tab(MAIN_TAB_LEARN)
                    st.session_state.session_loaded_msg = f"Loaded session: {loaded['topic']}"
                    st.rerun()
                else:
                    st.error("Session code not found.")

        recents = session_manager.list_recent_sessions(limit=5)
        other_recents = [r for r in recents if r["session_id"] != st.session_state.session_id]
        if other_recents:
            st.markdown("##### 🕒 Recent Study Sessions:")
            for r in other_recents:
                t_str = time.strftime("%b %d, %H:%M", time.localtime(r["updated_at"]))
                rev_n = r.get("needs_review_count", 0)
                rev_suffix = f" | 🔄 {rev_n}" if rev_n > 0 else ""
                xp_n = r.get("xp_points", 0)
                xp_suffix = f" | ⚡ {xp_n} XP" if xp_n > 0 else ""
                c_lbl = f"{r['topic'][:14]}... (🏆 {r['completed_count']}/{r['total_tenses']}{xp_suffix})"
                if st.button(f"▶️ {c_lbl}", key=f"rec_btn_{r['session_id']}", help=f"Code: {r['session_id']} | Updated: {t_str}", use_container_width=True):
                    loaded = session_manager.load_session(r["session_id"])
                    if loaded:
                        st.session_state.session_id = r["session_id"]
                        st.query_params["sid"] = r["session_id"]
                        st.session_state.current_curriculum = loaded["current_curriculum"]
                        st.session_state.active_tense_index = loaded["active_tense_index"]
                        st.session_state.active_card_step = loaded["active_card_step"]
                        st.session_state.completed_tenses = set(loaded["completed_tenses"])
                        st.session_state.needs_review_tenses = set(loaded.get("needs_review_tenses", []))
                        st.session_state.completed_card_steps = set(loaded["completed_card_steps"])
                        st.session_state.chat_history = loaded["chat_history"]
                        st.session_state.xp_points = loaded.get("xp_points", 0)
                        st.session_state.awarded_xp_events = set()
                        st.session_state.current_pack = None
                        st.session_state.pack_cache = {}
                        st.session_state.speech_eval_result = None
                        st.session_state.quiz_eval_result = None
                        safe_set_main_tab(MAIN_TAB_LEARN)
                        st.session_state.session_loaded_msg = f"Resumed: {loaded['topic']}"
                        st.rerun()

        st.markdown("---")
        if st.button("🔄 Reset progress and start over", use_container_width=True):
            st.session_state.active_tense_index = 0
            st.session_state.active_card_step = 1
            st.session_state.completed_card_steps = set()
            st.session_state.completed_tenses = set()
            st.session_state.needs_review_tenses = set()
            st.session_state.current_pack = None
            st.session_state.speech_eval_result = None
            st.session_state.quiz_eval_result = None
            safe_set_main_tab(MAIN_TAB_LEARN)
            auto_save_current_session()
            st.rerun()

        # Observability & Visual Element (VE) Telemetry (Google Frontend Standard)
        is_debug_mode = (st.query_params.get("debug") == "true" or st.query_params.get("dev") == "true")
        if is_debug_mode:
            st.markdown("---")
            st.caption("🛠️ **Developer Telemetry (VE)**")
            ve_logs = st.session_state.get("ve_logs", [])
            if ve_logs:
                for log in reversed(ve_logs[-6:]):
                    meta_str = f" | {log['metadata']}" if log['metadata'] else ""
                    st.markdown(f"<div class='telemetry-row'><code>{log['timestamp']}</code> [{log['action']}] <strong>{log['ve_id']}</strong>{meta_str}</div>", unsafe_allow_html=True)
            else:
                st.caption("No events logged yet. Interact with curriculum cards to generate telemetry.")
            
            if st.button("Clear telemetry logs", key="clear_telemetry_btn", use_container_width=True):
                st.session_state.ve_logs = []
                st.rerun()

"""

code = code.replace(old_sidebar_code, new_sidebar_code, 1)

# 3. Top Navigation Bar in Main Area Layout
old_main_top = """# Main Area Layout
rank_info = session_manager.get_rank_for_xp(st.session_state.get("xp_points", 0))
col_hdr_brand, col_hdr_xp = st.columns([2.6, 1.4])
with col_hdr_brand:
    st.markdown('<h1 class="main-title" style="margin-bottom: 2px;">🎓 LingoCraft AI</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title" style="margin-bottom: 12px; font-size: 0.95rem;">Interactive foreign language coach with 5-stage active recall & speech practice</p>', unsafe_allow_html=True)
with col_hdr_xp:
    xp_val = st.session_state.get("xp_points", 0)
    st.markdown(f\"\"\"
    <div style="background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 14px; padding: 8px 14px; box-shadow: 0 1px 3px rgba(60,64,67,0.06); display: flex; flex-direction: column; align-items: flex-end; justify-content: center; margin-top: 4px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="font-weight: 700; color: #174EA6; font-size: 1rem;">⚡ {xp_val} XP</span>
            <span class="badge-active" style="font-size: 0.78rem;">{rank_info['icon']} Lvl {rank_info['level']}: {rank_info['name']}</span>
        </div>
        <div style="font-size: 0.72rem; color: #5F6368; margin-top: 4px;">
            {rank_info['current_xp']} / {rank_info['next_level_xp']} XP to next level
        </div>
    </div>
    \"\"\", unsafe_allow_html=True)
    st.progress(rank_info['progress_ratio'])"""

new_main_top = """# Main Area Layout - Sleek Top Navigation Bar
rank_info = session_manager.get_rank_for_xp(st.session_state.get("xp_points", 0))
cur_topic = st.session_state.current_curriculum.get("topic", "Spanish: Verbo 'Hacer'")
target_l = st.session_state.current_curriculum.get("target_language", "Spanish")
flag_emoji = "🇪🇸" if "span" in target_l.lower() else ("🇧🇷" if "portug" in target_l.lower() else "🇬🇧")

col_hdr_brand, col_hdr_center, col_hdr_xp = st.columns([1.6, 2.2, 1.8], vertical_alignment="center")

with col_hdr_brand:
    st.markdown('<div style="display: flex; align-items: center; gap: 8px;"><span style="font-size: 1.7rem;">🎓</span> <span style="font-size: 1.35rem; font-weight: 700; color: #174EA6; letter-spacing: -0.02rem;">LingoCraft</span></div>', unsafe_allow_html=True)

with col_hdr_center:
    st.markdown(f\"\"\"
    <div style="background: #F8F9FA; border: 1px solid #DADCE0; border-radius: 9999px; padding: 5px 14px; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 1px 2px rgba(60,64,67,0.04);">
        <span style="font-size: 1.05rem;">{flag_emoji}</span>
        <span style="font-weight: 600; color: #202124; font-size: 0.88rem;">{cur_topic}</span>
    </div>
    \"\"\", unsafe_allow_html=True)

with col_hdr_xp:
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
        with st.popover("ℹ️", use_container_width=True, help="About LingoCraft AI"):
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

assert old_main_top in code, "Could not find old_main_top in app.py"
code = code.replace(old_main_top, new_main_top, 1)

# 4. Remove redundant interactive stepper from tab_curriculum
old_tab_curr_stepper = """    st.markdown("---")
    st.markdown("### 🎯 Interactive tenses stepper")
    st.caption("Click any tense below to jump directly to its 5-stage flashcard study:")

    # Top Stepper Bar (Clickable Stage Buttons with 3-Tier Status)
    c_cols = st.columns(min(len(roadmap), 5)) if roadmap else []
    for i, t in enumerate(roadmap):
        with c_cols[i % len(c_cols)]:
            is_act = (i == st.session_state.active_tense_index)
            is_comp = (i in st.session_state.completed_tenses)
            is_rev = (i in st.session_state.needs_review_tenses)

            if is_act:
                icon = "🎯 "
            elif is_comp:
                icon = "🏆 "
            elif is_rev:
                icon = "🔄 "
            else:
                icon = "⏳ "

            btn_t = "primary" if is_act else "secondary"
            st.button(
                f"{icon}Stage {i+1}\\n{t}",
                key=f"curr_stepper_btn_{i}",
                use_container_width=True,
                type=btn_t,
                on_click=select_tense_and_study,
                args=(i, 1),
                help=f"Click to study Stage {i+1}: {t}"
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📚 Stages overview")"""

new_tab_curr_stepper = """    st.markdown("---")
    st.markdown("### 📚 Syllabus & Stages Overview")
    st.caption("Detailed breakdown of all roadmap stages. Select any stage to study or review:")"""

assert old_tab_curr_stepper in code, "Could not find old_tab_curr_stepper in app.py"
code = code.replace(old_tab_curr_stepper, new_tab_curr_stepper, 1)

with open("app.py", "w") as f:
    f.write(code)

print("Roadmap and banner redesign applied successfully!")
