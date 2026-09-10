"""
LingoCraft AI - Streamlit Application.
Interactive, empathetic, tense-by-tense language learning coach with 5-stage flashcard system.
"""
import streamlit as st
import os
import json
import random
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import LingoCraft AI components
from lingocraft_agent import LingoCraftOrchestrator
from curriculum_data import SPANISH_HACER_CURRICULUM, CURATED_CURRICULA, get_curriculum_or_fallback
from audio_utils import generate_tts_audio, transcribe_audio_bytes

# Set page configuration
st.set_page_config(
    page_title="LingoCraft AI — Language Learning Coach",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .main-title {
        font-size: 2.3rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .card-container {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.5rem;
    }
    .stage-badge {
        display: inline-block;
        background-color: #EEF2FF;
        color: #4338CA;
        font-weight: 600;
        font-size: 0.85rem;
        padding: 4px 12px;
        border-radius: 9999px;
        margin-bottom: 12px;
        border: 1px solid #C7D2FE;
    }
    .phonetic-box {
        background-color: #F8FAFC;
        border-left: 4px solid #6366F1;
        padding: 14px 18px;
        border-radius: 6px;
        font-family: monospace;
        font-size: 1.15rem;
        color: #1E293B;
        margin: 12px 0;
    }
    .feedback-box-success {
        background-color: #ECFDF5;
        border: 1px solid #A7F3D0;
        border-radius: 8px;
        padding: 16px;
        color: #065F46;
        margin-top: 14px;
    }
    .feedback-box-error {
        background-color: #FEF2F2;
        border: 1px solid #FECACA;
        border-radius: 8px;
        padding: 16px;
        color: #991B1B;
        margin-top: 14px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GEMINI_API_KEY", "")

if "current_curriculum" not in st.session_state:
    st.session_state.current_curriculum = {
        "topic": SPANISH_HACER_CURRICULUM.title,
        "target_language": SPANISH_HACER_CURRICULUM.target_language,
        "target_language_code": SPANISH_HACER_CURRICULUM.target_language_code,
        "native_language": SPANISH_HACER_CURRICULUM.native_language,
        "description": SPANISH_HACER_CURRICULUM.description,
        "tenses_roadmap": SPANISH_HACER_CURRICULUM.tenses_roadmap,
    }

if "active_tense_index" not in st.session_state:
    st.session_state.active_tense_index = 0

if "active_card_step" not in st.session_state:
    st.session_state.active_card_step = 1  # 1 to 5

if "completed_card_steps" not in st.session_state:
    st.session_state.completed_card_steps = set()

if "completed_tenses" not in st.session_state:
    st.session_state.completed_tenses = set()

if "current_pack" not in st.session_state:
    st.session_state.current_pack = None

if "speech_eval_result" not in st.session_state:
    st.session_state.speech_eval_result = None

if "quiz_eval_result" not in st.session_state:
    st.session_state.quiz_eval_result = None

if "micro_practice_result" not in st.session_state:
    st.session_state.micro_practice_result = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Initialize Orchestrator
orchestrator = LingoCraftOrchestrator(api_key=st.session_state.api_key)

# Sidebar
with st.sidebar:
    st.title("⚙️ Learning Setup")

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

    if not st.session_state.api_key:
        st.info("💡 Using **Curated Offline Mastery Packs**. Enter a Gemini API Key above for custom topics!")

    st.markdown("---")
    st.subheader("📚 Topic & Language Pair")

    study_mode = st.radio("Select Curriculum Mode:", ["Curated Core Topics", "Custom Topic (AI Powered)"])

    if study_mode == "Curated Core Topics":
        curated_choices = [
            "Spanish: Irregular Verbs — Verbo 'Hacer'",
            "Spanish: 'Ser' vs 'Estar' (Essentials)",
            "French: Verbe Irrégulier — 'Aller'",
            "German: Modalverben — 'Können'",
            "Portuguese: Verbo Irregular — 'Fazer'",
            "Italian: Verbi Irregolari — 'Fare'"
        ]
        chosen_topic = st.selectbox("Choose a Curated Topic:", curated_choices)
        curated_native = st.selectbox("Your Native / Support Language:", ["English", "Portuguese", "Spanish", "French"])

        if st.button("Load Selected Curriculum", use_container_width=True):
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
                target_l = chosen_topic.split(":")[0].strip()
                plan = orchestrator.initialize_curriculum(chosen_topic, target_l, curated_native)
                st.session_state.current_curriculum = plan

            st.session_state.active_tense_index = 0
            st.session_state.active_card_step = 1
            st.session_state.completed_card_steps = set()
            st.session_state.current_pack = None
            st.session_state.completed_tenses = set()
            st.session_state.speech_eval_result = None
            st.session_state.quiz_eval_result = None
            st.rerun()

    else:
        custom_target = st.selectbox("Target Language:", ["Spanish", "French", "German", "Italian", "Portuguese", "Japanese", "Other"])
        custom_native = st.selectbox("Native / Support Language:", ["English", "Spanish", "Portuguese", "French"])
        custom_topic_text = st.text_input("Topic Description:", "Irregular Verbs: Verbo 'Tener'")

        if st.button("🚀 Initialize Custom Curriculum", use_container_width=True):
            with st.spinner("Initializing Curriculum Roadmap with LingoCraft AI..."):
                plan = orchestrator.initialize_curriculum(custom_topic_text, custom_target, custom_native)
                st.session_state.current_curriculum = plan
                st.session_state.active_tense_index = 0
                st.session_state.active_card_step = 1
                st.session_state.completed_card_steps = set()
                st.session_state.current_pack = None
                st.session_state.completed_tenses = set()
                st.session_state.speech_eval_result = None
                st.session_state.quiz_eval_result = None
                st.success("Roadmap successfully initialized!")
                st.rerun()

    st.markdown("---")
    st.subheader("🗺️ Pedagogical Roadmap")
    roadmap = st.session_state.current_curriculum.get("tenses_roadmap", [])
    for idx, tense in enumerate(roadmap):
        if idx in st.session_state.completed_tenses:
            st.markdown(f"✅ **{idx+1}. {tense}** (Mastered)")
        elif idx == st.session_state.active_tense_index:
            st.markdown(f"🎯 **{idx+1}. {tense}** *(In Progress)*")
        else:
            st.markdown(f"⏳ {idx+1}. {tense}")

    st.markdown("---")
    if st.button("🔄 Reset Progress / Start Over", use_container_width=True):
        st.session_state.active_tense_index = 0
        st.session_state.active_card_step = 1
        st.session_state.completed_card_steps = set()
        st.session_state.completed_tenses = set()
        st.session_state.current_pack = None
        st.session_state.speech_eval_result = None
        st.session_state.quiz_eval_result = None
        st.rerun()

# Main Area Layout
st.markdown('<div class="main-title">🎓 LingoCraft AI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive, empathetic, tense-by-tense foreign language coach using an enhanced 5-stage flashcard system.</div>', unsafe_allow_html=True)

# Main Navigation Tabs
tab_learn, tab_coach, tab_curriculum = st.tabs(["📖 5-Stage Flashcard Study", "💬 Ask Coach LingoCraft", "🗺️ Curriculum Overview"])

with tab_curriculum:
    st.subheader(f"Topic: {st.session_state.current_curriculum.get('topic')}")
    st.write(f"**Target Language:** {st.session_state.current_curriculum.get('target_language')} | **Native / Support Language:** {st.session_state.current_curriculum.get('native_language')}")
    st.info(st.session_state.current_curriculum.get("description", ""))
    st.markdown("### Tenses Sequence in this Pack:")
    for i, t in enumerate(roadmap):
        status = "✅ Mastered" if i in st.session_state.completed_tenses else ("🎯 Active" if i == st.session_state.active_tense_index else "⏳ Upcoming")
        st.markdown(f"- **Stage {i+1}: {t}** — {status}")

with tab_coach:
    curr_tense_name = roadmap[st.session_state.active_tense_index] if roadmap else "General"
    st.subheader("💬 Empathetic Language Coach")
    st.markdown("Ask any questions about the current tense, grammar doubts, cultural usage, or request additional practice sentences!")

    # Contextual Smart Follow-up Questions (reloaded on every tense/pack change)
    coach_prompts = []
    if st.session_state.current_pack and hasattr(st.session_state.current_pack, "suggested_coach_prompts"):
        coach_prompts = st.session_state.current_pack.suggested_coach_prompts

    if coach_prompts:
        st.markdown(f"##### 💡 Smart Follow-up Questions for **{curr_tense_name}**:")
        p_cols = st.columns(min(len(coach_prompts), 3))
        for p_idx, prompt_text in enumerate(coach_prompts[:3]):
            with p_cols[p_idx]:
                if st.button(f"👉 {prompt_text}", key=f"quick_prompt_{curr_tense_name}_{p_idx}", use_container_width=True):
                    st.session_state.chat_history.append({"role": "user", "content": prompt_text})
                    with st.spinner("Coach LingoCraft is typing..."):
                        ans = orchestrator.ask_coach(
                            question=prompt_text,
                            current_topic=st.session_state.current_curriculum.get("topic", ""),
                            current_tense=curr_tense_name,
                            target_lang=st.session_state.current_curriculum.get("target_language", "Spanish"),
                            native_lang=st.session_state.current_curriculum.get("native_language", "English"),
                            chat_history=st.session_state.chat_history
                        )
                        st.session_state.chat_history.append({"role": "assistant", "content": ans})
                    st.rerun()

    st.markdown("---")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_query := st.chat_input("Ask Coach LingoCraft a question (e.g. 'Why is this form irregular?' or 'Give me 3 examples'):"):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Coach LingoCraft is typing..."):
                ans = orchestrator.ask_coach(
                    question=user_query,
                    current_topic=st.session_state.current_curriculum.get("topic", ""),
                    current_tense=curr_tense_name,
                    target_lang=st.session_state.current_curriculum.get("target_language", "Spanish"),
                    native_lang=st.session_state.current_curriculum.get("native_language", "English"),
                    chat_history=st.session_state.chat_history
                )
                st.markdown(ans)
                st.session_state.chat_history.append({"role": "assistant", "content": ans})

with tab_learn:
    # Check if all tenses completed
    if len(st.session_state.completed_tenses) >= len(roadmap) and len(roadmap) > 0:
        st.balloons()
        st.success("🎉 ¡Felicitaciones! You have successfully mastered all tenses in this curriculum!")
        st.markdown(f"### Summary of Mastery: **{st.session_state.current_curriculum.get('topic')}**")
        st.write("You have conquered each grammatical form with pronunciation, speech validation, and conjugation quiz challenges.")
        if st.button("Review or Study Another Topic ➔"):
            st.session_state.active_tense_index = 0
            st.session_state.active_card_step = 1
            st.session_state.completed_card_steps = set()
            st.session_state.completed_tenses = set()
            st.rerun()
    else:
        # Get active tense
        current_tense_name = roadmap[st.session_state.active_tense_index]

        # Load card pack if needed
        if st.session_state.current_pack is None or st.session_state.current_pack.tense_name != current_tense_name:
            with st.spinner(f"Generating 5-Stage Flashcard Pack for **{current_tense_name}**..."):
                pack = orchestrator.load_tense_card_pack(
                    topic=st.session_state.current_curriculum.get("topic", ""),
                    tense_name=current_tense_name,
                    tense_order=st.session_state.active_tense_index + 1,
                    target_lang=st.session_state.current_curriculum.get("target_language", "Spanish"),
                    native_lang=st.session_state.current_curriculum.get("native_language", "English")
                )
                st.session_state.current_pack = pack

        pack = st.session_state.current_pack

        # Display Tense Header with direct skip/master option
        col_hdr_title, col_hdr_skip = st.columns([3, 1])
        with col_hdr_title:
            st.markdown(f"### 🎯 Tense {st.session_state.active_tense_index + 1} of {len(roadmap)}: **{current_tense_name}**")
        with col_hdr_skip:
            if st.button("🏆 Mark Tense Mastered ➔", help="Jump to the next tense if you already know this form", use_container_width=True):
                st.session_state.completed_tenses.add(st.session_state.active_tense_index)
                st.session_state.active_tense_index += 1
                st.session_state.active_card_step = 1
                st.session_state.completed_card_steps = set()
                st.session_state.current_pack = None
                st.session_state.speech_eval_result = None
                st.session_state.quiz_eval_result = None
                st.rerun()

        # Step 1: Interactive Stepper (allows jumping directly to any card!)
        step_cols = st.columns(5)
        step_names = ["1. Concept & Rule", "2. Bilingual Example", "3. Pronunciation Guide", "4. Speech Validation", "5. Conjugation Quiz"]
        for s_idx, col in enumerate(step_cols):
            with col:
                step_num = s_idx + 1
                is_active = (step_num == st.session_state.active_card_step)
                is_completed = (step_num in st.session_state.completed_card_steps)
                icon = "🎯 " if is_active else ("✓ " if is_completed else "")
                btn_type = "primary" if is_active else "secondary"
                if st.button(f"{icon}{step_names[s_idx]}", key=f"stepper_{current_tense_name}_{step_num}", use_container_width=True, type=btn_type):
                    st.session_state.active_card_step = step_num
                    st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # Flashcard Container
        st.markdown('<div class="card-container">', unsafe_allow_html=True)

        target_l = st.session_state.current_curriculum.get("target_language", "Target Language")
        native_l = st.session_state.current_curriculum.get("native_language", "Native Language")

        # -------------------------------------------------------------
        # STAGE 1: CONCEPT & RULE
        # -------------------------------------------------------------
        if st.session_state.active_card_step == 1:
            st.markdown('<span class="stage-badge">CARD 1 OF 5: CONCEPT & RULE</span>', unsafe_allow_html=True)
            st.markdown(f"## {pack.card1_concept.title}")

            st.markdown("#### 📌 Grammatical Rule & Structure")
            st.markdown(pack.card1_concept.rule)

            st.markdown("#### 🌍 Real-World Usage Context")
            st.markdown(pack.card1_concept.usage_context)

            st.markdown("#### 🔑 Common Trigger Keywords")
            for trig in pack.card1_concept.triggers:
                st.markdown(f"- `{trig}`")

            st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
            col_a, col_skip, col_b = st.columns([2, 2, 1])
            with col_skip:
                if st.button("⏩ Mark Complete & Jump to Next", key="jump_c1", use_container_width=True):
                    st.session_state.completed_card_steps.add(1)
                    st.session_state.active_card_step = 2
                    st.rerun()
            with col_b:
                if st.button("Next: Example ➔", use_container_width=True, type="primary"):
                    st.session_state.completed_card_steps.add(1)
                    st.session_state.active_card_step = 2
                    st.rerun()

        # -------------------------------------------------------------
        # STAGE 2: BILINGUAL EXAMPLE (Neutral Labels)
        # -------------------------------------------------------------
        elif st.session_state.active_card_step == 2:
            st.markdown('<span class="stage-badge">CARD 2 OF 5: BILINGUAL EXAMPLE</span>', unsafe_allow_html=True)
            st.markdown("## Real-World Comparative Phrase")

            st.markdown(f"#### 🎯 Target Language ({target_l}):")
            st.markdown(f"<div style='font-size:1.4rem; font-weight:600; color:#1E3A8A; background-color:#EFF6FF; padding:16px; border-radius:8px; border-left:5px solid #3B82F6;'>{pack.card2_example.target_sentence}</div>", unsafe_allow_html=True)

            st.markdown(f"#### 🌐 Translation / Meaning ({native_l}):")
            st.markdown(f"<div style='font-size:1.15rem; color:#374151; background-color:#F9FAFB; padding:14px; border-radius:8px; margin-top:8px;'>{pack.card2_example.native_sentence}</div>", unsafe_allow_html=True)

            st.markdown("#### 🔍 Grammatical Breakdown & Nuance:")
            st.markdown(pack.card2_example.breakdown)

            st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
            col_prev, col_skip, col_next = st.columns([1, 2, 1])
            with col_prev:
                if st.button("⬅ Back to Concept", use_container_width=True):
                    st.session_state.active_card_step = 1
                    st.rerun()
            with col_skip:
                if st.button("⏩ Mark Complete & Jump to Next", key="jump_c2", use_container_width=True):
                    st.session_state.completed_card_steps.add(2)
                    st.session_state.active_card_step = 3
                    st.rerun()
            with col_next:
                if st.button("Next: Pronunciation ➔", use_container_width=True, type="primary"):
                    st.session_state.completed_card_steps.add(2)
                    st.session_state.active_card_step = 3
                    st.rerun()

        # -------------------------------------------------------------
        # STAGE 3: PRONUNCIATION GUIDE
        # -------------------------------------------------------------
        elif st.session_state.active_card_step == 3:
            st.markdown('<span class="stage-badge">CARD 3 OF 5: PRONUNCIATION GUIDE</span>', unsafe_allow_html=True)
            st.markdown("## Phonetic Breakdown & Native Audio")

            st.markdown(f"### Key Verb / Phrase: **{pack.card3_pronunciation.word}**")

            st.markdown("#### 🗣️ Syllables & Stress Pattern:")
            st.markdown(f"<div class='phonetic-box'>{pack.card3_pronunciation.phonetic_breakdown}</div>", unsafe_allow_html=True)
            st.info(f"Primary Stress falls on: **{pack.card3_pronunciation.stressed_syllables}**")

            st.markdown("#### 🎧 Spoken Audio Ready:")
            target_lang_code = st.session_state.current_curriculum.get("target_language_code", "es")
            audio_bytes = generate_tts_audio(pack.card3_pronunciation.audio_text, lang=target_lang_code)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")

            st.markdown("#### 💡 Phonetic Coaching Tips:")
            st.markdown(pack.card3_pronunciation.phonetic_tips)

            st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
            col_prev, col_skip, col_next = st.columns([1, 2, 1])
            with col_prev:
                if st.button("⬅ Back to Example", use_container_width=True):
                    st.session_state.active_card_step = 2
                    st.rerun()
            with col_skip:
                if st.button("⏩ Mark Complete & Jump to Next", key="jump_c3", use_container_width=True):
                    st.session_state.completed_card_steps.add(3)
                    st.session_state.active_card_step = 4
                    st.rerun()
            with col_next:
                if st.button("Next: Speech Validation ➔", use_container_width=True, type="primary"):
                    st.session_state.completed_card_steps.add(3)
                    st.session_state.active_card_step = 4
                    st.session_state.speech_eval_result = None
                    st.rerun()

        # -------------------------------------------------------------
        # STAGE 4: SPEECH VALIDATION
        # -------------------------------------------------------------
        elif st.session_state.active_card_step == 4:
            st.markdown('<span class="stage-badge">CARD 4 OF 5: SPEECH VALIDATION</span>', unsafe_allow_html=True)
            st.markdown("## Voice Practice & Speech Evaluation")

            st.markdown(f"Speak this sentence aloud:")
            st.markdown(f"<div style='font-size:1.35rem; font-weight:600; color:#1E3A8A; background-color:#EFF6FF; padding:16px; border-radius:8px;'>{pack.card4_speech.target_phrase}</div>", unsafe_allow_html=True)

            st.markdown(f"*Expected Phonetic Flow: `{pack.card4_speech.expected_phonetics}`*")
            st.caption(f"Focus Sounds: {pack.card4_speech.key_focus_sounds}")

            st.markdown("#### 🎙️ Record or Submit Your Voice:")

            voice_tab1, voice_tab2 = st.tabs(["Microphone Recording", "Text / Spoken Transcript"])

            with voice_tab1:
                try:
                    from streamlit_mic_recorder import mic_recorder
                    audio_record = mic_recorder(
                        start_prompt="🔴 Start Recording",
                        stop_prompt="⏹️ Stop Recording",
                        key=f"speech_mic_recorder_{current_tense_name}"
                    )
                    if audio_record:
                        st.audio(audio_record['bytes'])
                        transcribed = transcribe_audio_bytes(audio_record['bytes'], lang=st.session_state.current_curriculum.get("target_language_code", "es"))
                        if transcribed:
                            st.write(f"Transcribed Speech: **{transcribed}**")
                            if st.button("Evaluate Recorded Speech", key=f"eval_rec_{current_tense_name}"):
                                with st.spinner("LingoCraft AI Speech Validator analyzing phonetics..."):
                                    eval_res = orchestrator.validate_speech(
                                        spoken_text=transcribed,
                                        target_phrase=pack.card4_speech.target_phrase,
                                        target_lang=target_l,
                                        native_lang=native_l
                                    )
                                    st.session_state.speech_eval_result = eval_res
                        else:
                            st.warning("Speech could not be transcribed cleanly from recording. You can also type what you said in the next tab!")
                except Exception:
                    st.info("Microphone ready. You can also validate your speech in the text tab.")

            with voice_tab2:
                spoken_input = st.text_input("Type or confirm what you said:", value=pack.card4_speech.target_phrase, key=f"text_speech_{current_tense_name}")
                if st.button("Evaluate Pronunciation", key=f"eval_text_{current_tense_name}"):
                    with st.spinner("Evaluating pronunciation accuracy with Coach LingoCraft..."):
                        eval_res = orchestrator.validate_speech(
                            spoken_text=spoken_input,
                            target_phrase=pack.card4_speech.target_phrase,
                            target_lang=target_l,
                            native_lang=native_l
                        )
                        st.session_state.speech_eval_result = eval_res

            # Display speech validation result if present
            if st.session_state.speech_eval_result:
                res = st.session_state.speech_eval_result
                score = res.get("accuracy_score", 80)

                st.markdown("### Evaluation Feedback:")
                st.progress(score / 100)
                st.write(f"**Accuracy Score:** {score}%")

                if score >= 75:
                    st.markdown(f"<div class='feedback-box-success'><h4>{res.get('feedback_title', '¡Excelente!')}</h4><p>{res.get('evaluation_message')}</p><p><strong>Tip:</strong> {res.get('actionable_tip')}</p></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='feedback-box-error'><h4>{res.get('feedback_title', 'Constructive Feedback')}</h4><p>{res.get('evaluation_message')}</p><p><strong>Adjustment:</strong> {res.get('actionable_tip')}</p></div>", unsafe_allow_html=True)
                    if res.get("requires_micro_practice") and res.get("micro_practice_drill"):
                        st.warning(f"🔄 **Immediate Micro-Practice:** {res.get('micro_practice_drill')}")

            st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
            col_prev, col_skip, col_next = st.columns([1, 2, 1])
            with col_prev:
                if st.button("⬅ Back to Pronunciation", use_container_width=True):
                    st.session_state.active_card_step = 3
                    st.rerun()
            with col_skip:
                if st.button("⏩ Mark Complete & Jump to Quiz", key="jump_c4", use_container_width=True):
                    st.session_state.completed_card_steps.add(4)
                    st.session_state.active_card_step = 5
                    st.session_state.quiz_eval_result = None
                    st.session_state.micro_practice_result = None
                    st.rerun()
            with col_next:
                if st.button("Next: Conjugation Quiz ➔", use_container_width=True, type="primary"):
                    st.session_state.completed_card_steps.add(4)
                    st.session_state.active_card_step = 5
                    st.session_state.quiz_eval_result = None
                    st.session_state.micro_practice_result = None
                    st.rerun()

        # -------------------------------------------------------------
        # STAGE 5: CONJUGATION QUIZ (Shuffled Options & No Pre-selection)
        # -------------------------------------------------------------
        elif st.session_state.active_card_step == 5:
            st.markdown('<span class="stage-badge">CARD 5 OF 5: CONJUGATION QUIZ</span>', unsafe_allow_html=True)
            st.markdown("## Master Tense Conjugation Challenge")

            st.markdown("#### Fill in the blank with the correct form:")
            st.markdown(f"<div style='font-size:1.3rem; font-weight:500; color:#1F2937; background-color:#F3F4F6; padding:18px; border-radius:8px;'>{pack.card5_quiz.sentence_prompt}</div>", unsafe_allow_html=True)

            # Shuffle options persistently for this tense pack so option A is NOT always correct!
            quiz_shuffle_key = f"quiz_shuffled_{current_tense_name}"
            if quiz_shuffle_key not in st.session_state:
                opts = list(pack.card5_quiz.options)
                random.seed(len(current_tense_name) * 42)
                random.shuffle(opts)
                st.session_state[quiz_shuffle_key] = opts

            display_options = st.session_state[quiz_shuffle_key]

            # index=None forces user to actively pick an option (no spoilers!)
            quiz_choice = st.radio(
                "Choose the correct answer:",
                display_options,
                index=None,
                key=f"quiz_radio_{current_tense_name}"
            )

            col_submit, col_skip_t = st.columns([2, 1])
            with col_submit:
                if st.button("Submit Answer 🚀", type="primary", use_container_width=True):
                    if quiz_choice is None:
                        st.warning("⚠️ Please select an answer before submitting!")
                    else:
                        with st.spinner("Evaluating your answer with LingoCraft AI..."):
                            eval_res = orchestrator.evaluate_quiz(
                                quiz_data=pack.card5_quiz,
                                selected_option=quiz_choice,
                                target_lang=target_l,
                                native_lang=native_l
                            )
                            st.session_state.quiz_eval_result = eval_res
                            st.session_state.micro_practice_result = None

            with col_skip_t:
                if st.button("⏩ Skip & Mark Tense Complete", key="skip_quiz", use_container_width=True):
                    st.session_state.completed_card_steps.add(5)
                    st.session_state.completed_tenses.add(st.session_state.active_tense_index)
                    st.session_state.active_tense_index += 1
                    st.session_state.active_card_step = 1
                    st.session_state.completed_card_steps = set()
                    st.session_state.current_pack = None
                    st.session_state.speech_eval_result = None
                    st.session_state.quiz_eval_result = None
                    st.rerun()

            # Display Quiz Feedback
            if st.session_state.quiz_eval_result:
                qres = st.session_state.quiz_eval_result
                if qres["is_correct"]:
                    st.session_state.completed_card_steps.add(5)
                    st.markdown(f"<div class='feedback-box-success'><h3>{qres.get('headline')}</h3><p>{qres.get('feedback')}</p></div>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                    # Advance to Next Tense Button
                    if st.button("🏆 Complete Tense & Advance to Next ➔", type="primary", use_container_width=True):
                        st.session_state.completed_tenses.add(st.session_state.active_tense_index)
                        st.session_state.active_tense_index += 1
                        st.session_state.active_card_step = 1
                        st.session_state.completed_card_steps = set()
                        st.session_state.current_pack = None
                        st.session_state.speech_eval_result = None
                        st.session_state.quiz_eval_result = None
                        st.rerun()

                else:
                    st.markdown(f"<div class='feedback-box-error'><h3>{qres.get('headline')}</h3><p>{qres.get('feedback')}</p><p><strong>Why this mistake is common:</strong> {qres.get('why_common_mistake')}</p></div>", unsafe_allow_html=True)

                    # Immediate Micro-Practice Drill
                    if qres.get("micro_practice_prompt"):
                        st.markdown("--- ")
                        st.markdown("### 🛠️ Immediate Micro-Practice Drill")
                        st.markdown(f"**{qres.get('micro_practice_prompt')}**")
                        mp_options = qres.get("micro_practice_options", [])
                        if mp_options:
                            user_mp_choice = st.radio("Select the micro-practice answer:", mp_options, index=None, key=f"mp_radio_{current_tense_name}")
                            if st.button("Verify Micro-Practice"):
                                if user_mp_choice is None:
                                    st.warning("⚠️ Please select an option first!")
                                else:
                                    correct_mp_idx = qres.get("micro_practice_correct_index", 0)
                                    if user_mp_choice == mp_options[correct_mp_idx]:
                                        st.success(f"¡Bien hecho! {qres.get('micro_practice_explanation')}")
                                        st.session_state.micro_practice_result = True
                                    else:
                                        st.error("Not quite yet. Remember the core rule and try once more!")

                        if st.session_state.micro_practice_result:
                            if st.button("Now Advance to Next Tense ➔"):
                                st.session_state.completed_card_steps.add(5)
                                st.session_state.completed_tenses.add(st.session_state.active_tense_index)
                                st.session_state.active_tense_index += 1
                                st.session_state.active_card_step = 1
                                st.session_state.completed_card_steps = set()
                                st.session_state.current_pack = None
                                st.session_state.speech_eval_result = None
                                st.session_state.quiz_eval_result = None
                                st.rerun()

            st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
            col_prev, col_space = st.columns([1, 4])
            with col_prev:
                if st.button("⬅ Back to Speech", use_container_width=True):
                    st.session_state.active_card_step = 4
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)
