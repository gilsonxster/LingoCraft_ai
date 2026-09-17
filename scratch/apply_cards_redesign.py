with open("app.py", "r") as f:
    code = f.read()

# Replace _flashcard_study_fragment stepper and Card 1
old_frag_start = """def _flashcard_study_fragment(pack, current_tense_name: str, total_tenses: int):
    \"\"\"
    Isolated Streamlit fragment for flashcard study (stepper and card content).
    Interactions here execute in-place without triggering a full page rerun by default.
    \"\"\"
    step_names = [
        "1. Concept & rule",
        "2. Bilingual example",
        "3. Pronunciation guide",
        "4. Speech validation",
        "5. Conjugation quiz"
    ]
    # Step 1: Interactive Stepper (allows jumping directly to any card)
    step_cols = st.columns(5)
    for s_idx, col in enumerate(step_cols):
        with col:
            step_num = s_idx + 1
            is_active = (step_num == st.session_state.active_card_step)
            is_completed = (step_num in st.session_state.completed_card_steps)
            icon = "🎯 " if is_active else ("✓ " if is_completed else "")
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}{step_names[s_idx]}", key=f"stepper_{current_tense_name}_{step_num}", use_container_width=True, type=btn_type):
                st.session_state.active_card_step = step_num
                auto_save_current_session()
                log_ve_event("stepper_card_jump", "click", {"step": step_num})
                st.rerun(scope="fragment")

    target_l = st.session_state.current_curriculum.get("target_language", "Target Language")
    native_l = st.session_state.current_curriculum.get("native_language", "Native Language")

    # -------------------------------------------------------------
    # STAGE 1: CONCEPT & RULE
    # -------------------------------------------------------------
    if st.session_state.active_card_step == 1:
        st.markdown(f"## {pack.card1_concept.title}")

        st.markdown("#### 📌 Grammatical rule & structure")
        st.markdown(pack.card1_concept.rule)

        # Full Person Conjugation Table / List (1st, 2nd, and 3rd person)
        conjugations = getattr(pack.card1_concept, "conjugations", [])
        if conjugations:
            is_pt_card = "portugu" in native_l.lower()
            section_label = "Conjugação completa do verbo (1ª, 2ª e 3ª pessoa)" if is_pt_card else "Full verb conjugation (1st, 2nd & 3rd person)"
            sg_label = "👤 Singular (1ª, 2ª, 3ª pessoa)" if is_pt_card else "👤 Singular (1st, 2nd, 3rd person)"
            pl_label = "👥 Plural (1ª, 2ª, 3ª pessoa)" if is_pt_card else "👥 Plural (1st, 2nd, 3rd person)"

            st.markdown(f"#### 👥 {section_label}")
            conj_header = getattr(pack.card1_concept, "conjugation_header", None) or ("A conjugação é bastante irregular, mas muito comum:" if is_pt_card else "The conjugation features common irregular forms:")
            st.markdown(f"<div style='font-size: 0.95rem; font-weight: 500; color: var(--gmat-sys-color-text-secondary); margin-bottom: 10px;'>{conj_header}</div>", unsafe_allow_html=True)

            rows_html = []
            for item in conjugations:
                m = re.match(r'^(.*?)\s*(\(.*?\))$', item.strip())
                if m:
                    target_part, native_part = m.group(1).strip(), m.group(2).strip()
                    rows_html.append(
                        f"<div style='display: flex; justify-content: space-between; align-items: center; background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 8px; padding: 8px 14px; margin: 4px 0; box-shadow: 0 1px 2px rgba(60,64,67,0.04);'>"
                        f"<span style='font-family: monospace; font-size: 1.02rem; font-weight: 700; color: #174EA6;'>{html.escape(target_part)}</span>"
                        f"<span style='font-size: 0.88rem; color: #5F6368; font-style: italic;'>{html.escape(native_part)}</span>"
                        f"</div>"
                    )
                else:
                    rows_html.append(
                        f"<div style='background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 8px; padding: 8px 14px; margin: 4px 0; font-family: monospace; font-size: 1rem; color: #174EA6; font-weight: 600;'>"
                        f"{html.escape(item)}"
                        f"</div>"
                    )

            if len(rows_html) == 6:
                col_sg, col_pl = st.columns(2)
                with col_sg:
                    st.markdown(f"<div style='font-size: 0.75rem; font-weight: 700; color: #5F6368; text-transform: uppercase; letter-spacing: 0.05rem; margin-bottom: 6px;'>{sg_label}</div>", unsafe_allow_html=True)
                    for r in rows_html[:3]:
                        st.markdown(r, unsafe_allow_html=True)
                with col_pl:
                    st.markdown(f"<div style='font-size: 0.75rem; font-weight: 700; color: #5F6368; text-transform: uppercase; letter-spacing: 0.05rem; margin-bottom: 6px;'>{pl_label}</div>", unsafe_allow_html=True)
                    for r in rows_html[3:]:
                        st.markdown(r, unsafe_allow_html=True)
            else:
                for r in rows_html:
                    st.markdown(r, unsafe_allow_html=True)

            st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

        st.markdown("#### 🌍 Real-world usage context")
        st.markdown(pack.card1_concept.usage_context)

        with st.expander("🔑 Linguistic Triggers & Keywords", expanded=True):
            trigger_pills = " ".join([f"<span style='display:inline-block; background-color:#F1F3F4; color:#202124; padding:3px 10px; border-radius:16px; margin:2px 4px; font-family:monospace; font-size:0.875rem; border:1px solid #DADCE0;'>{trig}</span>" for trig in pack.card1_concept.triggers])
            st.markdown(trigger_pills, unsafe_allow_html=True)

        render_incontext_coach(current_tense_name, 1, pack, target_l, native_l)

        st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
        col_space, col_next = st.columns([3, 1.4])
        with col_next:
            if st.button("Next: bilingual example ➔", key="next_c1", use_container_width=True, type="primary"):
                st.session_state.completed_card_steps.add(1)
                st.session_state.active_card_step = 2
                auto_save_current_session()
                st.rerun(scope="fragment")"""

new_frag_start = """def _flashcard_study_fragment(pack, current_tense_name: str, total_tenses: int):
    \"\"\"
    Isolated Streamlit fragment for flashcard study (stepper and card content).
    Interactions here execute in-place without triggering a full page rerun by default.
    \"\"\"
    step_labels = [
        "1. Rule",
        "2. Example",
        "3. Pronounce",
        "4. Speech",
        "5. Quiz"
    ]
    # Step 1: Horizontal Progress Stepper
    step_cols = st.columns(5)
    for s_idx, col in enumerate(step_cols):
        with col:
            step_num = s_idx + 1
            is_active = (step_num == st.session_state.active_card_step)
            is_completed = (step_num in st.session_state.completed_card_steps)
            icon = "● " if is_active else ("✓ " if is_completed else "")
            btn_type = "primary" if is_active else "secondary"
            if st.button(f"{icon}{step_labels[s_idx]}", key=f"stepper_{current_tense_name}_{step_num}", use_container_width=True, type=btn_type):
                st.session_state.active_card_step = step_num
                auto_save_current_session()
                log_ve_event("stepper_card_jump", "click", {"step": step_num})
                st.rerun(scope="fragment")

    st.progress(st.session_state.active_card_step / 5.0)

    target_l = st.session_state.current_curriculum.get("target_language", "Target Language")
    native_l = st.session_state.current_curriculum.get("native_language", "Native Language")
    is_infinitivo = "infinitivo" in current_tense_name.lower()

    # -------------------------------------------------------------
    # STAGE 1: CONCEPT & RULE
    # -------------------------------------------------------------
    if st.session_state.active_card_step == 1:
        col_c1_title, col_c1_coach = st.columns([3.2, 1.2])
        with col_c1_title:
            st.markdown(f"<h3 style='margin: 8px 0 4px 0; color: #174EA6; font-size: 1.35rem;'>{pack.card1_concept.title}</h3>", unsafe_allow_html=True)
        with col_c1_coach:
            render_incontext_coach(current_tense_name, 1, pack, target_l, native_l)

        st.markdown("#### 📌 Grammatical rule & structure")
        st.markdown(pack.card1_concept.rule)

        # Full Person Conjugation Table / List (1st, 2nd, and 3rd person) OR Infinitive Structures
        conjugations = getattr(pack.card1_concept, "conjugations", [])
        if conjugations:
            is_pt_card = "portugu" in native_l.lower()
            if is_infinitivo:
                section_label = "Estruturas essenciais com Infinitivo (Perífrases e Modais)" if is_pt_card else "Essential Infinitive Verbal Structures & Periphrases"
                col1_label = "📌 Perífrases com Verbo Auxiliar" if is_pt_card else "📌 Modal & Auxiliary Periphrases"
                col2_label = "🔗 Preposições + Infinitivo" if is_pt_card else "🔗 Prepositional Structures"
                conj_header = getattr(pack.card1_concept, "conjugation_header", None) or (
                    "O infinitivo é a forma base não conjugada. Usado diretamente após verbos auxiliares e preposições:" if is_pt_card
                    else "The infinitive is the unconjugated base form. Used directly after modal verbs and prepositions:"
                )
            else:
                section_label = "Conjugação completa do verbo (1ª, 2ª e 3ª pessoa)" if is_pt_card else "Full verb conjugation (1st, 2nd & 3rd person)"
                col1_label = "👤 Singular (1ª, 2ª, 3ª pessoa)" if is_pt_card else "👤 Singular (1st, 2nd, 3rd person)"
                col2_label = "👥 Plural (1ª, 2ª, 3ª pessoa)" if is_pt_card else "👥 Plural (1st, 2nd, 3rd person)"
                conj_header = getattr(pack.card1_concept, "conjugation_header", None) or (
                    "A conjugação é bastante irregular, mas muito comum:" if is_pt_card
                    else "The conjugation features common irregular forms:"
                )

            st.markdown(f"#### 👥 {section_label}")
            st.markdown(f"<div style='font-size: 0.95rem; font-weight: 500; color: var(--gmat-sys-color-text-secondary); margin-bottom: 10px;'>{conj_header}</div>", unsafe_allow_html=True)

            rows_html = []
            for item in conjugations:
                m = re.match(r'^(.*?)\\s*(\\(.*?\\))$', item.strip())
                if m:
                    target_part, native_part = m.group(1).strip(), m.group(2).strip()
                    rows_html.append(
                        f"<div style='display: flex; justify-content: space-between; align-items: center; background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 8px; padding: 8px 14px; margin: 4px 0; box-shadow: 0 1px 2px rgba(60,64,67,0.04);'>"
                        f"<span style='font-family: monospace; font-size: 1.02rem; font-weight: 700; color: #174EA6;'>{html.escape(target_part)}</span>"
                        f"<span style='font-size: 0.88rem; color: #5F6368; font-style: italic;'>{html.escape(native_part)}</span>"
                        f"</div>"
                    )
                else:
                    rows_html.append(
                        f"<div style='background: #FFFFFF; border: 1px solid #DADCE0; border-radius: 8px; padding: 8px 14px; margin: 4px 0; font-family: monospace; font-size: 1rem; color: #174EA6; font-weight: 600;'>"
                        f"{html.escape(item)}"
                        f"</div>"
                    )

            if len(rows_html) == 6:
                col_sg, col_pl = st.columns(2)
                with col_sg:
                    st.markdown(f"<div style='font-size: 0.75rem; font-weight: 700; color: #5F6368; text-transform: uppercase; letter-spacing: 0.05rem; margin-bottom: 6px;'>{col1_label}</div>", unsafe_allow_html=True)
                    for r in rows_html[:3]:
                        st.markdown(r, unsafe_allow_html=True)
                with col_pl:
                    st.markdown(f"<div style='font-size: 0.75rem; font-weight: 700; color: #5F6368; text-transform: uppercase; letter-spacing: 0.05rem; margin-bottom: 6px;'>{col2_label}</div>", unsafe_allow_html=True)
                    for r in rows_html[3:]:
                        st.markdown(r, unsafe_allow_html=True)
            else:
                for r in rows_html:
                    st.markdown(r, unsafe_allow_html=True)

            st.markdown("<div style='margin-bottom: 14px;'></div>", unsafe_allow_html=True)

        st.markdown("#### 🌍 Real-world usage context")
        st.markdown(pack.card1_concept.usage_context)

        with st.expander("🔑 Linguistic Triggers & Keywords", expanded=True):
            trigger_pills = " ".join([f"<span style='display:inline-block; background-color:#F1F3F4; color:#202124; padding:3px 10px; border-radius:16px; margin:2px 4px; font-family:monospace; font-size:0.875rem; border:1px solid #DADCE0;'>{trig}</span>" for trig in pack.card1_concept.triggers])
            st.markdown(trigger_pills, unsafe_allow_html=True)

        st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
        col_space, col_next = st.columns([2.5, 1.5])
        with col_next:
            if st.button("Next: Bilingual Example ➔", key="next_c1", use_container_width=True, type="primary"):
                st.session_state.completed_card_steps.add(1)
                st.session_state.active_card_step = 2
                auto_save_current_session()
                st.rerun(scope="fragment")"""

assert old_frag_start in code, "Could not find old_frag_start in app.py"
code = code.replace(old_frag_start, new_frag_start, 1)

# Clean up Card 2 header & coach placement
old_c2 = """    elif st.session_state.active_card_step == 2:
        st.markdown("## Real-World Comparative Phrase")"""
new_c2 = """    elif st.session_state.active_card_step == 2:
        col_c2_title, col_c2_coach = st.columns([3.2, 1.2])
        with col_c2_title:
            st.markdown("<h3 style='margin: 8px 0 4px 0; color: #174EA6; font-size: 1.35rem;'>Real-World Comparative Phrase</h3>", unsafe_allow_html=True)
        with col_c2_coach:
            render_incontext_coach(current_tense_name, 2, pack, target_l, native_l)"""
assert old_c2 in code, "Could not find old_c2"
code = code.replace(old_c2, new_c2, 1)
# Remove bottom render_incontext_coach in Card 2
old_c2_coach_bot = """        with st.expander("🔍 Grammatical Structure & Breakdown", expanded=True):
            st.markdown(pack.card2_example.breakdown)

        render_incontext_coach(current_tense_name, 2, pack, target_l, native_l)"""
new_c2_coach_bot = """        with st.expander("🔍 Grammatical Structure & Breakdown", expanded=True):
            st.markdown(pack.card2_example.breakdown)"""
assert old_c2_coach_bot in code, "Could not find old_c2_coach_bot"
code = code.replace(old_c2_coach_bot, new_c2_coach_bot, 1)

# Clean up Card 3 header & coach placement
old_c3 = """    elif st.session_state.active_card_step == 3:
        st.markdown("## Phonetic Breakdown & Native Audio")"""
new_c3 = """    elif st.session_state.active_card_step == 3:
        col_c3_title, col_c3_coach = st.columns([3.2, 1.2])
        with col_c3_title:
            st.markdown("<h3 style='margin: 8px 0 4px 0; color: #174EA6; font-size: 1.35rem;'>Phonetic Breakdown & Native Audio</h3>", unsafe_allow_html=True)
        with col_c3_coach:
            render_incontext_coach(current_tense_name, 3, pack, target_l, native_l)"""
assert old_c3 in code, "Could not find old_c3"
code = code.replace(old_c3, new_c3, 1)
# Remove bottom render_incontext_coach in Card 3
old_c3_coach_bot = """        with st.expander("🗣️ Articulation & Vocal Coaching Tips", expanded=False):
            st.markdown(pack.card3_pronunciation.phonetic_tips)

        render_incontext_coach(current_tense_name, 3, pack, target_l, native_l)"""
new_c3_coach_bot = """        with st.expander("🗣️ Articulation & Vocal Coaching Tips", expanded=False):
            st.markdown(pack.card3_pronunciation.phonetic_tips)"""
assert old_c3_coach_bot in code, "Could not find old_c3_coach_bot"
code = code.replace(old_c3_coach_bot, new_c3_coach_bot, 1)

# Clean up Card 4 header & coach placement
old_c4 = """    elif st.session_state.active_card_step == 4:
        st.markdown("## Voice Practice & Speech Evaluation")"""
new_c4 = """    elif st.session_state.active_card_step == 4:
        col_c4_title, col_c4_coach = st.columns([3.2, 1.2])
        with col_c4_title:
            st.markdown("<h3 style='margin: 8px 0 4px 0; color: #174EA6; font-size: 1.35rem;'>Voice Practice & Speech Evaluation</h3>", unsafe_allow_html=True)
        with col_c4_coach:
            render_incontext_coach(current_tense_name, 4, pack, target_l, native_l)"""
assert old_c4 in code, "Could not find old_c4"
code = code.replace(old_c4, new_c4, 1)
# Remove bottom render_incontext_coach in Card 4
old_c4_coach_bot = """        _speech_practice_fragment(current_tense_name, pack, target_l, native_l)

        render_incontext_coach(current_tense_name, 4, pack, target_l, native_l)"""
new_c4_coach_bot = """        _speech_practice_fragment(current_tense_name, pack, target_l, native_l)"""
assert old_c4_coach_bot in code, "Could not find old_c4_coach_bot"
code = code.replace(old_c4_coach_bot, new_c4_coach_bot, 1)

# Clean up Card 5 header & coach placement
old_c5 = """    elif st.session_state.active_card_step == 5:
        st.markdown("## Master Tense Conjugation Challenge")"""
new_c5 = """    elif st.session_state.active_card_step == 5:
        col_c5_title, col_c5_coach = st.columns([3.2, 1.2])
        with col_c5_title:
            st.markdown("<h3 style='margin: 8px 0 4px 0; color: #174EA6; font-size: 1.35rem;'>Master Tense Conjugation Challenge</h3>", unsafe_allow_html=True)
        with col_c5_coach:
            render_incontext_coach(current_tense_name, 5, pack, target_l, native_l)"""
assert old_c5 in code, "Could not find old_c5"
code = code.replace(old_c5, new_c5, 1)
# Remove bottom render_incontext_coach in Card 5
old_c5_coach_bot = """        render_incontext_coach(current_tense_name, 5, pack, target_l, native_l)

        st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)"""
new_c5_coach_bot = """        st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)"""
assert old_c5_coach_bot in code, "Could not find old_c5_coach_bot"
code = code.replace(old_c5_coach_bot, new_c5_coach_bot, 1)

with open("app.py", "w") as f:
    f.write(code)

print("Card redesign successfully applied!")
