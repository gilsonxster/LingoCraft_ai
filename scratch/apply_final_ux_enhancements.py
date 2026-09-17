with open("app.py", "r") as f:
    code = f.read()

# 1. Sidebar study_mode radio -> segmented_control
old_sidebar_mode = """    study_mode = st.radio("Select Curriculum Mode:", ["Curated Core Topics", "Custom Topic (AI Powered)"])

    if study_mode == "Curated Core Topics":"""

new_sidebar_mode = """    study_mode = st.segmented_control(
        "Select Curriculum Mode:",
        ["Curated Core Topics", "Custom Topic (AI Powered)"],
        default="Curated Core Topics",
        label_visibility="collapsed"
    )
    if not study_mode:
        study_mode = "Curated Core Topics"

    if study_mode == "Curated Core Topics":"""

assert old_sidebar_mode in code, "Could not find old_sidebar_mode"
code = code.replace(old_sidebar_mode, new_sidebar_mode, 1)

# 2. VE Telemetry gated behind ?debug=true or ?dev=true
old_ve_block = """    # Observability & Visual Element (VE) Telemetry (Google Frontend Standard)
    with st.expander("📊 Observability & Telemetry (VE)", expanded=False):
        st.caption("Tracks user interaction events and performance telemetry following Google frontend standards.")
        ve_logs = st.session_state.get("ve_logs", [])
        if ve_logs:
            for log in reversed(ve_logs[-6:]):
                meta_str = f" | {log['metadata']}" if log['metadata'] else ""
                st.markdown(f"<div class='telemetry-row'><code>{log['timestamp']}</code> [{log['action']}] <strong>{log['ve_id']}</strong>{meta_str}</div>", unsafe_allow_html=True)
        else:
            st.caption("No events logged yet. Interact with curriculum cards to generate telemetry.")
        
        if st.button("Clear telemetry logs", key="clear_telemetry_btn", use_container_width=True):
            st.session_state.ve_logs = []
            st.rerun()"""

new_ve_block = """    # Observability & Visual Element (VE) Telemetry (Google Frontend Standard)
    # Gated behind ?debug=true or ?dev=true so language learners enjoy an uncluttered interface
    is_debug_mode = (st.query_params.get("debug") == "true" or st.query_params.get("dev") == "true")
    if is_debug_mode:
        with st.expander("🛠️ Developer Telemetry (VE)", expanded=False):
            st.caption("Tracks user interaction events and performance telemetry following Google frontend standards.")
            ve_logs = st.session_state.get("ve_logs", [])
            if ve_logs:
                for log in reversed(ve_logs[-6:]):
                    meta_str = f" | {log['metadata']}" if log['metadata'] else ""
                    st.markdown(f"<div class='telemetry-row'><code>{log['timestamp']}</code> [{log['action']}] <strong>{log['ve_id']}</strong>{meta_str}</div>", unsafe_allow_html=True)
            else:
                st.caption("No events logged yet. Interact with curriculum cards to generate telemetry.")
            
            if st.button("Clear telemetry logs", key="clear_telemetry_btn", use_container_width=True):
                st.session_state.ve_logs = []
                st.rerun()"""

assert old_ve_block in code, "Could not find old_ve_block"
code = code.replace(old_ve_block, new_ve_block, 1)

# 3. Main Area Header Gamification Consolidation
old_header = """# Main Area Layout
rank_info = session_manager.get_rank_for_xp(st.session_state.get("xp_points", 0))
st.markdown('<h1 class="main-title">🎓 LingoCraft AI</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">Interactive foreign language coach with 5-stage active recall & speech practice. <span class="xp-badge">⚡ <strong>{st.session_state.get("xp_points", 0)} XP</strong> · {rank_info["label"]}</span></p>', unsafe_allow_html=True)"""

new_header = """# Main Area Layout
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

assert old_header in code, "Could not find old_header"
code = code.replace(old_header, new_header, 1)

# 4. tab_curriculum button consolidation (40 buttons -> 1 primary + 1 popover)
old_curr_buttons = """        col_act1, col_act2, col_act3, col_act4 = st.columns([2.2, 1.8, 1.5, 1.5])
        with col_act1:
            btn_label = f"📖 {'Continue' if is_act else ('Review' if (is_comp or is_rev) else 'Start')} study ({t}) ➔"
            btn_t = "primary" if is_act else "secondary"
            st.button(
                btn_label,
                key=f"curr_card_study_{i}",
                use_container_width=True,
                type=btn_t,
                on_click=select_tense_and_study,
                args=(i, 1)
            )
        with col_act2:
            st.button(
                f"💬 Ask coach about {t}",
                key=f"curr_card_coach_{i}",
                use_container_width=True,
                on_click=select_tense_and_coach,
                args=(i,)
            )
        with col_act3:
            toggle_text = "↩️ Mark active" if is_comp else "🏆 Mark mastered"
            st.button(
                toggle_text,
                key=f"curr_card_toggle_{i}",
                use_container_width=True,
                on_click=toggle_tense_mastery,
                args=(i,)
            )
        with col_act4:
            rev_text = "✓ Clear review" if is_rev else "🔄 Flag review"
            st.button(
                rev_text,
                key=f"curr_card_rev_{i}",
                use_container_width=True,
                on_click=toggle_tense_review,
                args=(i,)
            )
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)"""

new_curr_buttons = """        col_study, col_opts = st.columns([3.6, 1.2])
        with col_study:
            btn_label = f"📖 {'Continue' if is_act else ('Review' if (is_comp or is_rev) else 'Start')} study ({t}) ➔"
            btn_t = "primary" if is_act else "secondary"
            st.button(
                btn_label,
                key=f"curr_card_study_{i}",
                use_container_width=True,
                type=btn_t,
                on_click=select_tense_and_study,
                args=(i, 1)
            )
        with col_opts:
            with st.popover("⚙️ Options", use_container_width=True):
                st.button(
                    f"💬 Ask coach about {t}",
                    key=f"curr_card_coach_{i}",
                    use_container_width=True,
                    on_click=select_tense_and_coach,
                    args=(i,)
                )
                toggle_text = "↩️ Mark active" if is_comp else "🏆 Mark mastered"
                st.button(
                    toggle_text,
                    key=f"curr_card_toggle_{i}",
                    use_container_width=True,
                    on_click=toggle_tense_mastery,
                    args=(i,)
                )
                rev_text = "✓ Clear review" if is_rev else "🔄 Flag review"
                st.button(
                    rev_text,
                    key=f"curr_card_rev_{i}",
                    use_container_width=True,
                    on_click=toggle_tense_review,
                    args=(i,)
                )
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)"""

assert old_curr_buttons in code, "Could not find old_curr_buttons"
code = code.replace(old_curr_buttons, new_curr_buttons, 1)

# 5. tab_learn Stage Header Consolidation
old_stage_hdr = """        # Topic indicator & Stage Header
        topic_title = st.session_state.current_curriculum.get("topic", "Curriculum")
        st.caption(f"🗺️ Curriculum: **{topic_title}**")

        col_hdr_title, col_hdr_skip = st.columns([3, 1.2])
        with col_hdr_title:
            st.markdown(f"### 🎯 Stage {st.session_state.active_tense_index + 1} of {len(roadmap)}: **{current_tense_name}**")
        with col_hdr_skip:
            if st.button("🏆 Mark tense as mastered ➔", help="Jump to the next tense if you already know this form", use_container_width=True):"""

new_stage_hdr = """        # Consolidated Stage Header & Status Bar
        topic_title = st.session_state.current_curriculum.get("topic", "Curriculum")
        col_hdr_title, col_hdr_skip = st.columns([3.2, 1.3])
        with col_hdr_title:
            st.markdown(f\"\"\"
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 2px;">
                <span class="badge-active" style="font-size: 0.78rem; font-weight: 700;">Stage {st.session_state.active_tense_index + 1} of {len(roadmap)}</span>
                <span style="color: #5F6368; font-size: 0.85rem;">{topic_title}</span>
            </div>
            <h2 style="margin: 0 0 8px 0; color: #202124; font-size: 1.55rem; font-weight: 700;">{current_tense_name}</h2>
            \"\"\", unsafe_allow_html=True)
        with col_hdr_skip:
            if st.button("🏆 Mark mastered ➔", help="Jump to the next stage if you already know this form", use_container_width=True):"""

assert old_stage_hdr in code, "Could not find old_stage_hdr"
code = code.replace(old_stage_hdr, new_stage_hdr, 1)

with open("app.py", "w") as f:
    f.write(code)

print("All final UX enhancements applied cleanly!")
