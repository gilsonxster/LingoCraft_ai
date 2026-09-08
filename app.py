"""
LingoCraft AI - Streamlit Application.
Interactive, empathetic, tense-by-tense language learning coach with 5-stage flashcard system.
"""
import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import LingoCraft AI components
from lingocraft_agent import LingoCraftOrchestrator
from curriculum_data import SPANISH_HACER_CURRICULUM, CURATED_CURRICULA
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
    .tense-pill {
        display: inline-block;
        background-color: #F3F4F6;
        color: #374151;
        padding: 4px 10px;
        border-radius: 6px;
        font-size: 0.85rem;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    .tense-pill-active {
        background-color: #3B82F6;
        color: white;
        font-weight: 600;
    }
    .tense-pill-done {
        background-color: #10B981;
        color: white;
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
    # Default initial curriculum: Spanish Hacer
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
        if st.button("Load Selected Curriculum", use_container_width=True):
            if "Hacer" in chosen_topic or "Spanish" in chosen_topic:
                st.session_state.current_curriculum = {
                    "topic": SPANISH_HACER_CURRICULUM.title,
                    "target_language": SPANISH_HACER_CURRICULUM.target_language,
                    "target_language_code": SPANISH_HACER_CURRICULUM.target_language_code,
                    "native_language": SPANISH_HACER_CURRICULUM.native_language,
                    "description": SPANISH_HACER_CURRICULUM.description,
                    "tenses_roadmap": SPANISH_HACER_CURRICULUM.tenses_roadmap,
                }
            else:
                target_l = chosen_topic.split(":")[0]
                plan = orchestrator.initialize_curriculum(chosen_topic, target_l, "English")
                st.session_state.current_curriculum = plan

            st.session_state.active_tense_index = 0
            st.session_state.active_card_step = 1
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
    st.write(f"**Target Language:** {st.session_state.current_curriculum.get('target_language')} | **Native Language:** {st.session_state.current_curriculum.get('native_language')}")
    st.info(st.session_state.current_curriculum.get("description", ""))
    st.markdown("### Tenses Sequence in this Pack:")
    for i, t in enumerate(roadmap):
        status = "✅ Mastered" if i in st.session_state.completed_tenses else ("🎯 Active" if i == st.session_state.active_tense_index else "⏳ Upcoming")
        st.markdown(f"- **Stage {i+1}: {t}** — {status}")

with tab_coach:
    st.subheader("💬 Empathetic Language Coach")
    st.markdown("Ask any questions about the current tense, grammar doubts, cultural usage, or request additional practice sentences!")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_query := st.chat_input("Ask Coach LingoCraft a question (e.g. 'Why is haciendo used here?' or 'Give me another example'):"):
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Coach LingoCraft is typing..."):
                curr_tense = roadmap[st.session_state.active_tense_index] if roadmap else "General"
                ans = orchestrator.ask_coach(
                    question=user_query,
                    current_topic=st.session_state.current_curriculum.get("topic", ""),
                    current_tense=curr_tense,
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

        # Display Tense Header & Stepper
        st.markdown(f"### 🎯 Tense {st.session_state.active_tense_index + 1} of {len(roadmap)}: **{current_tense_name}**")
        
        # Step breadcrumb
        step_cols = st.columns(5)
        step_names = ["1. Concept & Rule", "2. Bilingual Example", "3. Pronunciation Guide", "4. Speech Validation", "5. Conjugation Quiz"]
        for s_idx, col in enumerate(step_cols):
            with col:
                if s_idx + 1 == st.session_state.active_card_step:
                    st.markdown(f"<div style='background-color:#4F46E5;color:white;text-align:center;padding:8px;border-radius:8px;font-weight:bold;'>{step_names[s_idx]}</div>", unsafe_allow_html=True)
                elif s_idx + 1 < st.session_state.active_card_step:
                    st.markdown(f"<div style='background-color:#10B981;color:white;text-align:center;padding:8px;border-radius:8px;'>✓ {step_names[s_idx]}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='background-color:#F3F4F6;color:#6B7280;text-align:center;padding:8px;border-radius:8px;'>{step_names[s_idx]}</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Flashcard Container
        st.markdown('<div class="card-container">', unsafe_allow_html=True)

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
            col_a, col_b = st.columns([4, 1])
            with col_b:
                if st.button("Next: Example ➔", use_container_width=True, type="primary"):
                    st.session_state.active_card_step = 2
                    st.rerun()

        # -------------------------------------------------------------
        # STAGE 2: BILINGUAL EXAMPLE
        # -------------------------------------------------------------
        elif st.session_state.active_card_step == 2:
            st.markdown('<span class="stage-badge">CARD 2 OF 5: BILINGUAL EXAMPLE</span>', unsafe_allow_html=True)
            st.markdown("## Real-World Comparative Phrase")

            st.markdown("#### 🇪🇸 Target Language:")
            st.markdown(f"<div style='font-size:1.4rem; font-weight:600; color:#1E3A8A; background-color:#EFF6FF; padding:16px; border-radius:8px; border-left:5px solid #3B82F6;'>{pack.card2_example.target_sentence}</div>", unsafe_allow_html=True)

            st.markdown("#### 🇬🇧 Native Language Translation:")
            st.markdown(f"<div style='font-size:1.15rem; color:#374151; background-color:#F9FAFB; padding:14px; border-radius:8px; margin-top:8px;'>{pack.card2_example.native_sentence}</div>", unsafe_allow_html=True)

            st.markdown("#### 🔍 Grammatical Breakdown & Nuance:")
            st.markdown(pack.card2_example.breakdown)

            st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
            col_prev, col_space, col_next = st.columns([1, 3, 1])
            with col_prev:
                if st.button("⬅ Back to Concept", use_container_width=True):
                    st.session_state.active_card_step = 1
                    st.rerun()
            with col_next:
                if st.button("Next: Pronunciation ➔", use_container_width=True, type="primary"):
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
            # Generate Audio
            target_lang_code = st.session_state.current_curriculum.get("target_language_code", "es")
            audio_bytes = generate_tts_audio(pack.card3_pronunciation.audio_text, lang=target_lang_code)
            if audio_bytes:
                st.audio(audio_bytes, format="audio/mp3")

            st.markdown("#### 💡 Phonetic Coaching Tips:")
            st.markdown(pack.card3_pronunciation.phonetic_tips)

            st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
            col_prev, col_space, col_next = st.columns([1, 3, 1])
            with col_prev:
                if st.button("⬅ Back to Example", use_container_width=True):
                    st.session_state.active_card_step = 2
                    st.rerun()
            with col_next:
                if st.button("Next: Speech Validation ➔", use_container_width=True, type="primary"):
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
            
            # Mic input or text fallback
            voice_tab1, voice_tab2 = st.tabs(["Microphone Recording", "Text / Spoken Transcript"])
            
            with voice_tab1:
                try:
                    from streamlit_mic_recorder import mic_recorder
                    audio_record = mic_recorder(
                        start_prompt="🔴 Start Recording",
                        stop_prompt="⏹️ Stop Recording",
                        key="speech_mic_recorder"
                    )
                    if audio_record:
                        st.audio(audio_record['bytes'])
                        transcribed = transcribe_audio_bytes(audio_record['bytes'], lang=st.session_state.current_curriculum.get("target_language_code", "es"))
                        if transcribed:
                            st.write(f"Transcribed Speech: **{transcribed}**")
                            if st.button("Evaluate Recorded Speech"):
                                with st.spinner("LingoCraft AI Speech Validator analyzing phonetics..."):
                                    eval_res = orchestrator.validate_speech(
                                        spoken_text=transcribed,
                                        target_phrase=pack.card4_speech.target_phrase,
                                        target_lang=st.session_state.current_curriculum.get("target_language", "Spanish"),
                                        native_lang=st.session_state.current_curriculum.get("native_language", "English")
                                    )
                                    st.session_state.speech_eval_result = eval_res
                        else:
                            st.warning("Speech could not be transcribed cleanly from recording. You can also type what you said in the next tab!")
                except Exception as e:
                    st.info("Microphone widget ready. You can also submit your transcribed speech in the text tab.")

            with voice_tab2:
                spoken_input = st.text_input("Type or confirm what you said:", value=pack.card4_speech.target_phrase)
                if st.button("Evaluate Pronunciation"):
                    with st.spinner("Evaluating pronunciation accuracy with Coach LingoCraft..."):
                        eval_res = orchestrator.validate_speech(
                            spoken_text=spoken_input,
                            target_phrase=pack.card4_speech.target_phrase,
                            target_lang=st.session_state.current_curriculum.get("target_language", "Spanish"),
                            native_lang=st.session_state.current_curriculum.get("native_language", "English")
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
            col_prev, col_space, col_next = st.columns([1, 3, 1])
            with col_prev:
                if st.button("⬅ Back to Pronunciation", use_container_width=True):
                    st.session_state.active_card_step = 3
                    st.rerun()
            with col_next:
                if st.button("Next: Conjugation Quiz ➔", use_container_width=True, type="primary"):
                    st.session_state.active_card_step = 5
                    st.session_state.quiz_eval_result = None
                    st.session_state.micro_practice_result = None
                    st.rerun()

        # -------------------------------------------------------------
        # STAGE 5: CONJUGATION QUIZ
        # -------------------------------------------------------------
        elif st.session_state.active_card_step == 5:
            st.markdown('<span class="stage-badge">CARD 5 OF 5: CONJUGATION QUIZ</span>', unsafe_allow_html=True)
            st.markdown("## Master Tense Conjugation Challenge")
            
            st.markdown("#### Fill in the blank with the correct form:")
            st.markdown(f"<div style='font-size:1.3rem; font-weight:500; color:#1F2937; background-color:#F3F4F6; padding:18px; border-radius:8px;'>{pack.card5_quiz.sentence_prompt}</div>", unsafe_allow_html=True)

            quiz_choice = st.radio(
                "Choose the correct answer:",
                pack.card5_quiz.options,
                key=f"quiz_options_{current_tense_name}"
            )

            if st.button("Submit Answer 🚀", type="primary"):
                with st.spinner("Evaluating your answer with LingoCraft AI..."):
                    eval_res = orchestrator.evaluate_quiz(
                        quiz_data=pack.card5_quiz,
                        selected_option=quiz_choice,
                        target_lang=st.session_state.current_curriculum.get("target_language", "Spanish"),
                        native_lang=st.session_state.current_curriculum.get("native_language", "English")
                    )
                    st.session_state.quiz_eval_result = eval_res
                    st.session_state.micro_practice_result = None

            # Display Quiz Feedback
            if st.session_state.quiz_eval_result:
                qres = st.session_state.quiz_eval_result
                if qres["is_correct"]:
                    st.markdown(f"<div class='feedback-box-success'><h3>{qres.get('headline')}</h3><p>{qres.get('feedback')}</p></div>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Advance to Next Tense Button
                    if st.button("🏆 Complete Tense & Advance to Next ➔", type="primary", use_container_width=True):
                        st.session_state.completed_tenses.add(st.session_state.active_tense_index)
                        st.session_state.active_tense_index += 1
                        st.session_state.active_card_step = 1
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
                            user_mp_choice = st.radio("Select the micro-practice answer:", mp_options, key="mp_radio")
                            if st.button("Verify Micro-Practice"):
                                correct_mp_idx = qres.get("micro_practice_correct_index", 0)
                                if user_mp_choice == mp_options[correct_mp_idx]:
                                    st.success(f"¡Bien hecho! {qres.get('micro_practice_explanation')}")
                                    st.session_state.micro_practice_result = True
                                else:
                                    st.error("Not quite yet. Remember the core rule and try once more!")
                        
                        if st.session_state.micro_practice_result:
                            if st.button("Now Advance to Next Tense ➔"):
                                st.session_state.completed_tenses.add(st.session_state.active_tense_index)
                                st.session_state.active_tense_index += 1
                                st.session_state.active_card_step = 1
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
