"""
LingoCraft AI - Streamlit Application.
Interactive, empathetic, tense-by-tense language learning coach with 5-stage flashcard system.
"""
import streamlit as st
import streamlit.components.v1 as components
import os
import json
import random
import time
from datetime import datetime
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Import LingoCraft AI components
import importlib
import session_manager
importlib.reload(session_manager)
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

# Custom Styling (Google Material Design 3 & 4px Spacing Tokens)
st.markdown("""
<style>
    /* ====================================================================
       Google Material 3 (GM3) & 4px Spacing Design Tokens
       ==================================================================== */
    :root {
        --gmat-sys-color-primary: #1A73E8;
        --gmat-sys-color-on-primary: #FFFFFF;
        --gmat-sys-color-primary-container: #E8F0FE;
        --gmat-sys-color-on-primary-container: #174EA6;
        --gmat-sys-color-surface: #FFFFFF;
        --gmat-sys-color-surface-variant: #F8F9FA;
        --gmat-sys-color-outline: #DADCE0;
        --gmat-sys-color-text-primary: #202124;
        --gmat-sys-color-text-secondary: #5F6368;
        --gmat-sys-color-success: #137333;
        --gmat-sys-color-success-container: #E6F4EA;
        --gmat-sys-color-error: #C5221F;
        --gmat-sys-color-error-container: #FCE8E6;
        --gmat-sys-color-warning: #B06000;
        --gmat-sys-color-warning-container: #FEF7E0;

        /* Strict 4px Spacing Scale */
        --space-1: 4px;
        --space-2: 8px;
        --space-3: 12px;
        --space-4: 16px;
        --space-5: 20px;
        --space-6: 24px;
        --space-8: 32px;
    }

    /* Accessibility focus rings */
    button:focus-visible, input:focus-visible, select:focus-visible, a:focus-visible {
        outline: 2px solid var(--gmat-sys-color-primary) !important;
        outline-offset: 2px !important;
    }

    .main-title {
        font-size: 2.25rem;
        font-weight: 700;
        color: #174EA6;
        margin-bottom: var(--space-1);
        letter-spacing: -0.02rem;
    }
    .sub-title {
        font-size: 1rem;
        color: var(--gmat-sys-color-text-secondary);
        margin-bottom: var(--space-6);
        line-height: 1.5;
    }
    .phonetic-box {
        background-color: var(--gmat-sys-color-surface-variant);
        border-left: 4px solid var(--gmat-sys-color-primary);
        padding: var(--space-4) var(--space-5);
        border-radius: 8px;
        font-family: monospace;
        font-size: 1.25rem;
        color: var(--gmat-sys-color-text-primary);
        margin: var(--space-3) 0;
        letter-spacing: 0.05rem;
    }
    .feedback-box-success {
        background-color: var(--gmat-sys-color-success-container);
        border: 1px solid #A8DAB5;
        border-radius: 12px;
        padding: var(--space-4);
        color: var(--gmat-sys-color-success);
        margin-top: var(--space-4);
    }
    .feedback-box-error {
        background-color: var(--gmat-sys-color-error-container);
        border: 1px solid #F6AEA9;
        border-radius: 12px;
        padding: var(--space-4);
        color: var(--gmat-sys-color-error);
        margin-top: var(--space-4);
    }
    .curriculum-card {
        background-color: var(--gmat-sys-color-surface);
        border: 1px solid var(--gmat-sys-color-outline);
        border-radius: 12px;
        padding: var(--space-4) var(--space-5);
        margin-top: var(--space-3);
        box-shadow: 0 1px 2px rgba(60, 64, 67, 0.05);
        transition: box-shadow 0.2s ease;
    }
    .curriculum-card:hover {
        box-shadow: 0 2px 6px rgba(60, 64, 67, 0.12);
    }
    .badge-mastered {
        background-color: var(--gmat-sys-color-success-container);
        color: var(--gmat-sys-color-success);
        border: 1px solid #A8DAB5;
        font-weight: 600;
        font-size: 0.8125rem;
        padding: 4px 10px;
        border-radius: 9999px;
    }
    .badge-review {
        background-color: var(--gmat-sys-color-warning-container);
        color: var(--gmat-sys-color-warning);
        border: 1px solid #F9AB00;
        font-weight: 600;
        font-size: 0.8125rem;
        padding: 4px 10px;
        border-radius: 9999px;
    }
    .badge-active {
        background-color: var(--gmat-sys-color-primary-container);
        color: var(--gmat-sys-color-on-primary-container);
        border: 1px solid #C2E7FF;
        font-weight: 600;
        font-size: 0.8125rem;
        padding: 4px 10px;
        border-radius: 9999px;
    }
    .badge-upcoming {
        background-color: var(--gmat-sys-color-surface-variant);
        color: var(--gmat-sys-color-text-secondary);
        border: 1px solid var(--gmat-sys-color-outline);
        font-weight: 600;
        font-size: 0.8125rem;
        padding: 4px 10px;
        border-radius: 9999px;
    }
    .diff-breakdown-card {
        background-color: var(--gmat-sys-color-surface-variant);
        border: 1px solid var(--gmat-sys-color-outline);
        border-radius: 12px;
        padding: var(--space-4);
        margin: var(--space-4) 0;
    }
    .diff-chip {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        padding: 4px 10px;
        border-radius: 8px;
        font-size: 0.95rem;
        font-weight: 500;
        margin: 2px 4px;
        transition: transform 0.15s ease;
    }
    .diff-chip:hover {
        transform: translateY(-1px);
    }
    .diff-match {
        background-color: var(--gmat-sys-color-success-container);
        color: var(--gmat-sys-color-success);
        border: 1px solid #A8DAB5;
    }
    .diff-near {
        background-color: #FEF7E0;
        color: #B06000;
        border: 1px solid #FEEFC3;
    }
    .diff-miss {
        background-color: var(--gmat-sys-color-error-container);
        color: var(--gmat-sys-color-error);
        border: 1px solid #F6AEA9;
    }
    .diff-omitted {
        background-color: #F1F3F4;
        color: #80868B;
        border: 1px dashed #DADCE0;
        text-decoration: line-through;
    }
    .diff-icon {
        font-weight: 700;
        font-size: 0.85rem;
    }
    .diff-heard {
        font-size: 0.8rem;
        font-style: italic;
        opacity: 0.85;
    }
    .incontext-coach-card {
        background-color: #F8FAFD;
        border: 1px solid #C2E7FF;
        border-radius: 12px;
        padding: var(--space-4);
        margin: var(--space-3) 0;
    }
    .telemetry-row {
        font-family: monospace;
        font-size: 0.75rem;
        color: #5F6368;
        padding: 4px 0;
        border-bottom: 1px solid #F1F3F4;
    }
    .xp-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: linear-gradient(135deg, #FEF7E0 0%, #FEEFC3 100%);
        color: #7C4A00;
        font-weight: 600;
        font-size: 0.8125rem;
        padding: 3px 12px;
        border-radius: 9999px;
        border: 1px solid #F9AB00;
        margin-left: 10px;
        box-shadow: 0 1px 2px rgba(60, 64, 67, 0.08);
        letter-spacing: 0.01rem;
    }
</style>
""", unsafe_allow_html=True)

# Tab Constants
MAIN_TAB_LEARN = "📖 5-Stage Flashcard Study"
MAIN_TAB_COACH = "💬 Ask Coach LingoCraft"
MAIN_TAB_CURRICULUM = "🗺️ Curriculum Overview"
MAIN_TAB_OPTIONS = [MAIN_TAB_LEARN, MAIN_TAB_COACH, MAIN_TAB_CURRICULUM]

TAB_KEY_TO_NAME = {
    "learn": MAIN_TAB_LEARN,
    "coach": MAIN_TAB_COACH,
    "curriculum": MAIN_TAB_CURRICULUM,
}

TAB_NAME_TO_KEY = {
    MAIN_TAB_LEARN: "learn",
    MAIN_TAB_COACH: "coach",
    MAIN_TAB_CURRICULUM: "curriculum",
}

# Visual Element (VE) Logging / Observability (Google Frontend Principle: "Log as you go")
def log_ve_event(ve_id: str, action: str = "impression", metadata: dict = None):
    if "ve_logs" not in st.session_state:
        st.session_state.ve_logs = []
    log_entry = {
        "timestamp": time.strftime("%H:%M:%S"),
        "ve_id": ve_id,
        "action": action,
        "metadata": metadata or {}
    }
    st.session_state.ve_logs.append(log_entry)
    if len(st.session_state.ve_logs) > 50:
        st.session_state.ve_logs.pop(0)

# Deep Linking & URL State Synchronization
def sync_url_params():
    """Synchronizes active session, tab, tense, and card step with URL query parameters."""
    if "session_id" in st.session_state and st.session_state.session_id:
        st.query_params["sid"] = st.session_state.session_id
    cur_tab = st.session_state.get("main_tab", MAIN_TAB_LEARN)
    st.query_params["tab"] = TAB_NAME_TO_KEY.get(cur_tab, "learn")
    st.query_params["tense"] = str(st.session_state.get("active_tense_index", 0))
    st.query_params["step"] = str(st.session_state.get("active_card_step", 1))

# Auto-save helper to persist progress into SQLite and synchronize URL parameters
def auto_save_current_session():
    if "session_id" in st.session_state and st.session_state.session_id:
        curr = st.session_state.get("current_curriculum", {})
        state_dict = {
            "current_curriculum": curr,
            "active_tense_index": st.session_state.get("active_tense_index", 0),
            "active_card_step": st.session_state.get("active_card_step", 1),
            "completed_tenses": list(st.session_state.get("completed_tenses", set())),
            "needs_review_tenses": list(st.session_state.get("needs_review_tenses", set())),
            "completed_card_steps": list(st.session_state.get("completed_card_steps", set())),
            "chat_history": st.session_state.get("chat_history", []),
            "xp_points": int(st.session_state.get("xp_points", 0)),
        }
        session_manager.save_session(st.session_state.session_id, state_dict)
    sync_url_params()

# Gamification: Idempotent XP Points Awarding
def award_xp(amount: int, event_id: str, reason: str):
    """
    Awards XP points idempotently per session so repeated interactions don't inflate scores.
    Triggers an instant celebratory toast and auto-saves progress.
    """
    if "awarded_xp_events" not in st.session_state:
        st.session_state.awarded_xp_events = set()
    if event_id not in st.session_state.awarded_xp_events:
        st.session_state.awarded_xp_events.add(event_id)
        st.session_state.xp_points = st.session_state.get("xp_points", 0) + amount
        auto_save_current_session()
        st.toast(f"⚡ +{amount} XP: {reason}!", icon="✨")
        log_ve_event("xp_awarded", "reward", {"amount": amount, "event_id": event_id, "total_xp": st.session_state.xp_points})

# Navigation Helper Callbacks
def select_tense_and_study(idx: int):
    st.session_state.active_tense_index = idx
    st.session_state.active_card_step = 1
    st.session_state.completed_card_steps = set()
    st.session_state.current_pack = None
    st.session_state.speech_eval_result = None
    st.session_state.quiz_eval_result = None
    st.session_state.main_tab = MAIN_TAB_LEARN
    auto_save_current_session()

def select_tense_and_coach(idx: int):
    st.session_state.active_tense_index = idx
    st.session_state.main_tab = MAIN_TAB_COACH
    auto_save_current_session()

def toggle_tense_mastery(idx: int):
    if idx in st.session_state.completed_tenses:
        st.session_state.completed_tenses.discard(idx)
    else:
        st.session_state.completed_tenses.add(idx)
        st.session_state.needs_review_tenses.discard(idx)
    auto_save_current_session()

def toggle_tense_review(idx: int):
    if idx in st.session_state.needs_review_tenses:
        st.session_state.needs_review_tenses.discard(idx)
    else:
        st.session_state.needs_review_tenses.add(idx)
        st.session_state.completed_tenses.discard(idx)
    auto_save_current_session()

def render_incontext_coach(current_tense_name: str, step_num: int, pack, target_l: str, native_l: str):
    """
    Renders an in-context Coach consultation widget directly inside the active flashcard container
    so learners can resolve doubts immediately without losing their card step or study flow.
    """
    with st.expander(f"💬 Ask Coach LingoCraft about {current_tense_name} (in-context)", expanded=False):
        st.markdown(f"<p style='font-size: 0.875rem; color: var(--gmat-sys-color-text-secondary); margin-bottom: 8px;'>Got a question about <strong>{current_tense_name}</strong>? Ask here and continue your study flow without switching tabs.</p>", unsafe_allow_html=True)

        prompts = getattr(pack, "suggested_coach_prompts", []) if pack else []
        if prompts:
            st.markdown("<div style='font-size: 0.8125rem; font-weight: 600; color: var(--gmat-sys-color-text-secondary); margin-bottom: 6px;'>💡 Quick questions:</div>", unsafe_allow_html=True)
            p_cols = st.columns(min(len(prompts[:3]), 3))
            for p_i, p_txt in enumerate(prompts[:3]):
                with p_cols[p_i]:
                    if st.button(f"👉 {p_txt}", key=f"inc_p_{current_tense_name}_{step_num}_{p_i}", use_container_width=True):
                        log_ve_event("incontext_coach_quick_prompt", "click", {"prompt": p_txt, "step": step_num})
                        with st.spinner("Coach LingoCraft is answering..."):
                            ans = orchestrator.ask_coach(
                                question=p_txt,
                                current_topic=st.session_state.current_curriculum.get("topic", ""),
                                current_tense=current_tense_name,
                                target_lang=target_l,
                                native_lang=native_l,
                                chat_history=st.session_state.chat_history
                            )
                            st.session_state[f"incontext_ans_{current_tense_name}_{step_num}"] = {
                                "q": p_txt,
                                "a": ans
                            }
                            st.session_state.chat_history.append({"role": "user", "content": p_txt})
                            st.session_state.chat_history.append({"role": "assistant", "content": ans})
                            auto_save_current_session()
                            st.rerun()

        col_q, col_btn = st.columns([4, 1.2])
        with col_q:
            custom_q = st.text_input(
                "Or type your question:",
                placeholder=f"e.g. Why does this form change in {current_tense_name}?",
                key=f"inc_q_input_{current_tense_name}_{step_num}",
                label_visibility="collapsed"
            )
        with col_btn:
            if st.button("Ask coach 💬", key=f"inc_btn_{current_tense_name}_{step_num}", use_container_width=True, type="primary"):
                if custom_q.strip():
                    log_ve_event("incontext_coach_custom_query", "submit", {"query": custom_q, "step": step_num})
                    with st.spinner("Coach LingoCraft is answering..."):
                        ans = orchestrator.ask_coach(
                            question=custom_q.strip(),
                            current_topic=st.session_state.current_curriculum.get("topic", ""),
                            current_tense=current_tense_name,
                            target_lang=target_l,
                            native_lang=native_l,
                            chat_history=st.session_state.chat_history
                        )
                        st.session_state[f"incontext_ans_{current_tense_name}_{step_num}"] = {
                            "q": custom_q.strip(),
                            "a": ans
                        }
                        st.session_state.chat_history.append({"role": "user", "content": custom_q.strip()})
                        st.session_state.chat_history.append({"role": "assistant", "content": ans})
                        auto_save_current_session()
                        st.rerun()

        step_ans_key = f"incontext_ans_{current_tense_name}_{step_num}"
        if step_ans_key in st.session_state and st.session_state[step_ans_key]:
            record = st.session_state[step_ans_key]
            st.markdown(f"""
            <div class="incontext-coach-card">
                <div style="font-weight: 600; font-size: 0.875rem; color: #174EA6; margin-bottom: 4px;">
                    🎓 Coach LingoCraft:
                </div>
                <div style="font-size: 0.8125rem; color: #5F6368; font-style: italic; margin-bottom: 8px;">
                    Regarding: "{record['q']}"
                </div>
                <div style="font-size: 0.95rem; color: #202124; line-height: 1.5;">
                    {record['a']}
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Clear coach response", key=f"clear_inc_{current_tense_name}_{step_num}", help="Dismiss this answer"):
                del st.session_state[step_ans_key]
                st.rerun()


# Resolve Session ID from URL query parameters (?sid=...) or restore active session
url_sid = st.query_params.get("sid", "").strip()

if "session_id" not in st.session_state:
    if url_sid:
        loaded_state = session_manager.load_session(url_sid)
        if loaded_state:
            st.session_state.session_id = url_sid
            st.session_state.current_curriculum = loaded_state["current_curriculum"]
            st.session_state.active_tense_index = loaded_state["active_tense_index"]
            st.session_state.active_card_step = loaded_state["active_card_step"]
            st.session_state.completed_tenses = set(loaded_state["completed_tenses"])
            st.session_state.needs_review_tenses = set(loaded_state.get("needs_review_tenses", []))
            st.session_state.completed_card_steps = set(loaded_state["completed_card_steps"])
            st.session_state.chat_history = loaded_state["chat_history"]
            st.session_state.session_loaded_msg = f"Resumed study session: {loaded_state['topic']}"
        else:
            st.session_state.session_id = url_sid
    else:
        st.session_state.session_id = session_manager.generate_session_id()

if "session_id" in st.session_state:
    st.query_params["sid"] = st.session_state.session_id

# Initialize Session State Variables
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

if "main_tab" not in st.session_state:
    st.session_state.main_tab = MAIN_TAB_LEARN

if "active_tense_index" not in st.session_state:
    st.session_state.active_tense_index = 0

if "active_card_step" not in st.session_state:
    st.session_state.active_card_step = 1  # 1 to 5

if "completed_card_steps" not in st.session_state:
    st.session_state.completed_card_steps = set()

if "completed_tenses" not in st.session_state:
    st.session_state.completed_tenses = set()

if "needs_review_tenses" not in st.session_state:
    st.session_state.needs_review_tenses = set()

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

if "xp_points" not in st.session_state:
    st.session_state.xp_points = 0

if "awarded_xp_events" not in st.session_state:
    st.session_state.awarded_xp_events = set()


# Synchronize session ID with browser localStorage to preserve state across browser restarts
components.html(f"""
<script>
  try {{
    const pLoc = window.parent.location;
    const sp = new URLSearchParams(pLoc.search);
    const sid = sp.get('sid');
    if (!sid) {{
      const cached = window.localStorage.getItem('lingocraft_sid');
      if (cached && cached.startsWith('lingo-')) {{
        pLoc.search = '?sid=' + encodeURIComponent(cached);
      }}
    }} else {{
      window.localStorage.setItem('lingocraft_sid', '{st.session_state.session_id}');
    }}
  }} catch(e) {{}}
</script>
""", height=0, width=0)

# Initialize Orchestrator defensively
orchestrator = LingoCraftOrchestrator(api_key=st.session_state.get("api_key", os.getenv("GEMINI_API_KEY", "")))

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

    # Study Session & Resume Widget
    with st.expander("💾 Study Session & Resume", expanded=False):
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
                st.session_state.speech_eval_result = None
                st.session_state.quiz_eval_result = None
                st.session_state.main_tab = MAIN_TAB_LEARN
                auto_save_current_session()
                st.rerun()
        with col_save_s:
            if st.button("💾 Save State", use_container_width=True):
                auto_save_current_session()
                st.toast("Progress saved to database!", icon="💾")

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
                    st.session_state.speech_eval_result = None
                    st.session_state.quiz_eval_result = None
                    st.session_state.main_tab = MAIN_TAB_LEARN
                    st.session_state.session_loaded_msg = f"Loaded session: {loaded['topic']}"
                    st.rerun()
                else:
                    st.error("Session code not found.")

        recents = session_manager.list_recent_sessions(limit=5)
        other_recents = [r for r in recents if r["session_id"] != st.session_state.session_id]
        if other_recents:
            st.markdown("---")
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
                        st.session_state.speech_eval_result = None
                        st.session_state.quiz_eval_result = None
                        st.session_state.main_tab = MAIN_TAB_LEARN
                        st.session_state.session_loaded_msg = f"Resumed: {loaded['topic']}"
                        st.rerun()

    st.markdown("---")
    st.subheader("📚 Topic & Language Pair")

    study_mode = st.radio("Select Curriculum Mode:", ["Curated Core Topics", "Custom Topic (AI Powered)"])

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
            st.session_state.needs_review_tenses = set()
            st.session_state.speech_eval_result = None
            st.session_state.quiz_eval_result = None
            st.session_state.main_tab = MAIN_TAB_LEARN
            auto_save_current_session()
            st.rerun()

    else:
        custom_target = st.selectbox("Target Language:", ["Spanish", "Portuguese", "English"])
        custom_native = st.selectbox("Native / Support Language:", ["English", "Portuguese", "Spanish"])
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
                st.session_state.needs_review_tenses = set()
                st.session_state.speech_eval_result = None
                st.session_state.quiz_eval_result = None
                st.session_state.main_tab = MAIN_TAB_LEARN
                auto_save_current_session()
                st.success("Roadmap successfully initialized!")
                st.rerun()

    st.markdown("---")
    st.subheader("🗺️ Pedagogical Roadmap")
    roadmap = st.session_state.current_curriculum.get("tenses_roadmap", [])
    total_tenses = len(roadmap)
    is_curriculum_completed = (
        total_tenses > 0 and (
            st.session_state.active_tense_index >= total_tenses
            or len(st.session_state.completed_tenses) >= total_tenses
        )
    )

    if roadmap:
        if 0 <= st.session_state.active_tense_index < total_tenses:
            active_tense_name = roadmap[st.session_state.active_tense_index]
        else:
            active_tense_name = roadmap[-1]
    else:
        active_tense_name = "General"

    needs_rev_set = st.session_state.get("needs_review_tenses", set())
    for idx, tense in enumerate(roadmap):
        is_act = (idx == st.session_state.active_tense_index)
        is_comp = (idx in st.session_state.completed_tenses)
        is_rev = (idx in needs_rev_set)

        if is_comp:
            label = f"🏆 {idx+1}. {tense}"
        elif is_rev:
            label = f"🔄 {idx+1}. {tense} (Review)"
        elif is_act:
            label = f"🎯 {idx+1}. {tense}"
        else:
            label = f"⏳ {idx+1}. {tense}"

        btn_t = "primary" if is_act else "secondary"
        st.button(
            label,
            key=f"sidebar_tense_{idx}",
            use_container_width=True,
            type=btn_t,
            on_click=select_tense_and_study,
            args=(idx,),
            help=f"Click to study Stage {idx+1}: {tense}"
        )

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
        st.session_state.main_tab = MAIN_TAB_LEARN
        auto_save_current_session()
        st.rerun()


    # Observability & Visual Element (VE) Telemetry (Google Frontend Standard)
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
            st.rerun()

# Display session loaded notification toast if set
if st.session_state.get("session_loaded_msg"):
    st.toast(f"💾 {st.session_state.session_loaded_msg}", icon="✅")
    st.session_state.session_loaded_msg = None

# Main Area Layout
rank_info = session_manager.get_rank_for_xp(st.session_state.get("xp_points", 0))
st.markdown('<h1 class="main-title">🎓 LingoCraft AI</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-title">Interactive foreign language coach with 5-stage active recall & speech practice. <span class="xp-badge">⚡ <strong>{st.session_state.get("xp_points", 0)} XP</strong> · {rank_info["label"]}</span></p>', unsafe_allow_html=True)

# Main Navigation Tabs
tab_learn, tab_coach, tab_curriculum = st.tabs(
    MAIN_TAB_OPTIONS,
    key="main_tab",
    on_change="rerun"
)

with tab_curriculum:
    log_ve_event("tab_curriculum_view", "impression")
    st.subheader(f"Topic: {st.session_state.current_curriculum.get('topic')}")
    col_meta1, col_meta2, col_meta3, col_meta4, col_meta5 = st.columns(5)
    with col_meta1:
        st.metric("Target language", st.session_state.current_curriculum.get('target_language', 'Spanish'))
    with col_meta2:
        st.metric("Native / Support", st.session_state.current_curriculum.get('native_language', 'English'))
    with col_meta3:
        comp_count = len(st.session_state.completed_tenses)
        st.metric("Mastered stages", f"{comp_count} / {total_tenses} Stages")
    with col_meta4:
        rev_count = len(st.session_state.needs_review_tenses)
        st.metric("Needs review", f"{rev_count} Stages")
    with col_meta5:
        st.metric("Experience (XP)", f"⚡ {st.session_state.get('xp_points', 0)} XP", delta=f"{rank_info['icon']} Lvl {rank_info['level']}")

    col_prog1, col_prog2 = st.columns(2)
    with col_prog1:
        st.caption(f"🗺️ Curriculum Completion: **{comp_count} / {total_tenses} Stages**")
        prog_val = comp_count / max(total_tenses, 1)
        st.progress(prog_val)
    with col_prog2:
        st.caption(f"🎖️ Craftsman Rank Progress: **{rank_info['name']}** ({rank_info['current_xp']} / {rank_info['next_level_xp']} XP)")
        st.progress(rank_info['progress_ratio'])

    st.info(st.session_state.current_curriculum.get("description", ""))

    st.markdown("---")
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
                f"{icon}Stage {i+1}\n{t}",
                key=f"curr_stepper_btn_{i}",
                use_container_width=True,
                type=btn_t,
                on_click=select_tense_and_study,
                args=(i, 1),
                help=f"Click to study Stage {i+1}: {t}"
            )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 📚 Stages overview")

    for i, t in enumerate(roadmap):
        is_act = (i == st.session_state.active_tense_index)
        is_comp = (i in st.session_state.completed_tenses)
        is_rev = (i in st.session_state.needs_review_tenses)

        if is_comp:
            badge_class = "badge-mastered"
            badge_label = "🏆 Mastered"
            border_color = "var(--gmat-sys-color-success)"
        elif is_rev:
            badge_class = "badge-review"
            badge_label = "🔄 Needs review"
            border_color = "var(--gmat-sys-color-warning)"
        elif is_act:
            badge_class = "badge-active"
            badge_label = "🎯 In progress (active)"
            border_color = "var(--gmat-sys-color-primary)"
        else:
            badge_class = "badge-upcoming"
            badge_label = "⏳ Upcoming"
            border_color = "var(--gmat-sys-color-outline)"

        st.markdown(f"""
        <div class="curriculum-card" style="border-left: 5px solid {border_color};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <h4 style="margin: 0; color: var(--gmat-sys-color-on-primary-container);">Stage {i+1}: {t}</h4>
                <span class="{badge_class}">{badge_label}</span>
            </div>
            <p style="color: var(--gmat-sys-color-text-secondary); margin: 4px 0 10px 0; font-size: 0.92rem;">
                <strong>5-stage mastery flow:</strong> 1. Concept & rule ➔ 2. Bilingual example ➔ 3. Pronunciation guide ➔ 4. Speech validation ➔ 5. Conjugation quiz
            </p>
        </div>
        """, unsafe_allow_html=True)

        col_act1, col_act2, col_act3, col_act4 = st.columns([2.2, 1.8, 1.5, 1.5])
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
        st.markdown("<div style='margin-bottom: 8px;'></div>", unsafe_allow_html=True)


with tab_coach:
    log_ve_event("tab_coach_view", "impression")
    curr_tense_name = active_tense_name
    st.subheader("💬 Empathetic Language Coach")
    st.markdown("Ask any questions about the current tense, grammar doubts, cultural usage, or request additional practice sentences.")

    # Contextual Smart Follow-up Questions (reloaded on every tense/pack change)
    coach_prompts = []
    if st.session_state.current_pack and hasattr(st.session_state.current_pack, "suggested_coach_prompts"):
        coach_prompts = st.session_state.current_pack.suggested_coach_prompts

    if coach_prompts:
        st.markdown(f"##### 💡 Smart follow-up questions for **{curr_tense_name}**:")
        p_cols = st.columns(min(len(coach_prompts), 3))
        for p_idx, prompt_text in enumerate(coach_prompts[:3]):
            with p_cols[p_idx]:
                if st.button(f"👉 {prompt_text}", key=f"quick_prompt_{curr_tense_name}_{p_idx}", use_container_width=True):
                    log_ve_event("coach_quick_prompt_click", "click", {"prompt": prompt_text})
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
                    auto_save_current_session()
                    st.rerun()

    st.markdown("---")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_query := st.chat_input("Ask Coach LingoCraft a question (for example, 'Why is this form irregular?' or 'Give me 3 examples'):"):
        log_ve_event("coach_query_submit", "submit")
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
        auto_save_current_session()

with tab_learn:
    log_ve_event("tab_learn_view", "impression", {
        "tense_index": st.session_state.active_tense_index,
        "card_step": st.session_state.active_card_step
    })

    # Check if all tenses completed
    if is_curriculum_completed:
        st.balloons()
        st.success("🎉 ¡Felicitaciones! You have successfully mastered all tenses in this curriculum!")
        st.markdown(f"### Summary of mastery: **{st.session_state.current_curriculum.get('topic')}**")
        st.write("You have conquered each grammatical form with pronunciation, speech validation, and conjugation quiz challenges.")
        col_rev, col_new = st.columns(2)
        with col_rev:
            if st.button("🔄 Review curriculum from start", use_container_width=True):
                st.session_state.active_tense_index = 0
                st.session_state.active_card_step = 1
                st.session_state.completed_card_steps = set()
                st.session_state.completed_tenses = set()
                st.session_state.current_pack = None
                st.session_state.speech_eval_result = None
                st.session_state.quiz_eval_result = None
                auto_save_current_session()
                st.rerun()
        with col_new:
            st.info("💡 You can also choose another topic or change language pairs anytime in the sidebar!")
    else:
        # Get active tense
        current_tense_name = active_tense_name

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

        # Step title lookup
        step_names = [
            "1. Concept & rule",
            "2. Bilingual example",
            "3. Pronunciation guide",
            "4. Speech validation",
            "5. Conjugation quiz"
        ]
        active_step_idx = st.session_state.active_card_step - 1
        active_step_label = step_names[active_step_idx] if 0 <= active_step_idx < len(step_names) else ""

        # Topic indicator & Stage Header
        topic_title = st.session_state.current_curriculum.get("topic", "Curriculum")
        st.caption(f"🗺️ Curriculum: **{topic_title}**")

        col_hdr_title, col_hdr_skip = st.columns([3, 1.2])
        with col_hdr_title:
            st.markdown(f"### 🎯 Stage {st.session_state.active_tense_index + 1} of {len(roadmap)}: **{current_tense_name}**")
        with col_hdr_skip:
            if st.button("🏆 Mark tense as mastered ➔", help="Jump to the next tense if you already know this form", use_container_width=True):
                award_xp(50, f"stage_mastered_{current_tense_name}", f"Stage mastered: {current_tense_name}")
                st.session_state.completed_tenses.add(st.session_state.active_tense_index)
                st.session_state.needs_review_tenses.discard(st.session_state.active_tense_index)
                st.session_state.active_tense_index += 1
                st.session_state.active_card_step = 1
                st.session_state.completed_card_steps = set()
                st.session_state.current_pack = None
                st.session_state.speech_eval_result = None
                st.session_state.quiz_eval_result = None
                auto_save_current_session()
                st.rerun()

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
                    st.rerun()

        target_l = st.session_state.current_curriculum.get("target_language", "Target Language")
        native_l = st.session_state.current_curriculum.get("native_language", "Native Language")

        # -------------------------------------------------------------
        # STAGE 1: CONCEPT & RULE
        # -------------------------------------------------------------
        if st.session_state.active_card_step == 1:
            st.markdown(f"## {pack.card1_concept.title}")

            st.markdown("#### 📌 Grammatical rule & structure")
            st.markdown(pack.card1_concept.rule)

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
                    st.rerun()

        # -------------------------------------------------------------
        # STAGE 2: BILINGUAL EXAMPLE
        # -------------------------------------------------------------
        elif st.session_state.active_card_step == 2:
            st.markdown("## Real-World Comparative Phrase")

            st.markdown(f"#### 🎯 Target language ({target_l}):")
            st.markdown(f"<div style='font-size:1.35rem; font-weight:600; color:#174EA6; background-color:#E8F0FE; padding:16px; border-radius:12px; border-left:5px solid #1A73E8;'>{pack.card2_example.target_sentence}</div>", unsafe_allow_html=True)

            target_lang_code = st.session_state.current_curriculum.get("target_language_code", "es")
            clean_audio_target = pack.card2_example.target_sentence.replace("**", "").replace("*", "")
            st.markdown("##### 🎧 Listen to phrase:")
            col_c2_a1, col_c2_a2 = st.columns(2)
            with col_c2_a1:
                st.caption("🔊 Normal speed (1.0x)")
                c2_audio_norm = generate_tts_audio(clean_audio_target, lang=target_lang_code, slow=False)
                if c2_audio_norm:
                    st.audio(c2_audio_norm, format="audio/mp3")
            with col_c2_a2:
                st.caption("🐢 Practice pace (0.75x)")
                c2_audio_slow = generate_tts_audio(clean_audio_target, lang=target_lang_code, slow=True)
                if c2_audio_slow:
                    st.audio(c2_audio_slow, format="audio/mp3")

            st.markdown(f"#### 🌐 Translation / Meaning ({native_l}):")
            st.markdown(f"<div style='font-size:1.125rem; color:#202124; background-color:#F8F9FA; padding:14px; border-radius:12px; margin-top:8px; border:1px solid #DADCE0;'>{pack.card2_example.native_sentence}</div>", unsafe_allow_html=True)

            with st.expander("🔍 Grammatical Structure & Breakdown", expanded=True):
                st.markdown(pack.card2_example.breakdown)

            render_incontext_coach(current_tense_name, 2, pack, target_l, native_l)

            st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
            col_prev, col_next = st.columns([1.2, 1.4])
            with col_prev:
                if st.button("⬅ Back to concept", key="back_c2", use_container_width=True):
                    st.session_state.active_card_step = 1
                    auto_save_current_session()
                    st.rerun()
            with col_next:
                if st.button("Next: pronunciation guide ➔", key="next_c2", use_container_width=True, type="primary"):
                    st.session_state.completed_card_steps.add(2)
                    st.session_state.active_card_step = 3
                    auto_save_current_session()
                    st.rerun()


        # -------------------------------------------------------------
        # STAGE 3: PRONUNCIATION GUIDE
        # -------------------------------------------------------------
        elif st.session_state.active_card_step == 3:
            st.markdown("## Phonetic Breakdown & Native Audio")

            st.markdown(f"### Key verb / phrase: **{pack.card3_pronunciation.word}**")

            st.markdown("#### 🗣️ Syllables & stress pattern:")
            st.markdown(f"<div class='phonetic-box'>{pack.card3_pronunciation.phonetic_breakdown}</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='margin-bottom:12px;'><span style='background-color:#E8F0FE; color:#174EA6; font-weight:600; padding:4px 12px; border-radius:9999px; font-size:0.875rem; border:1px solid #C2E7FF;'>Primary stress: {pack.card3_pronunciation.stressed_syllables}</span></div>", unsafe_allow_html=True)

            st.markdown("#### 🎧 Spoken audio (zero-latency cached):")
            target_lang_code = st.session_state.current_curriculum.get("target_language_code", "es")
            col_c3_a1, col_c3_a2 = st.columns(2)
            with col_c3_a1:
                st.caption("🔊 Normal speed (1.0x)")
                c3_audio_norm = generate_tts_audio(pack.card3_pronunciation.audio_text, lang=target_lang_code, slow=False)
                if c3_audio_norm:
                    st.audio(c3_audio_norm, format="audio/mp3")
            with col_c3_a2:
                st.caption("🐢 Practice pace (0.75x)")
                c3_audio_slow = generate_tts_audio(pack.card3_pronunciation.audio_text, lang=target_lang_code, slow=True)
                if c3_audio_slow:
                    st.audio(c3_audio_slow, format="audio/mp3")

            with st.expander("🗣️ Articulation & Vocal Coaching Tips", expanded=False):
                st.markdown(pack.card3_pronunciation.phonetic_tips)

            render_incontext_coach(current_tense_name, 3, pack, target_l, native_l)

            st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
            col_prev, col_next = st.columns([1.2, 1.4])
            with col_prev:
                if st.button("⬅ Back to example", key="back_c3", use_container_width=True):
                    st.session_state.active_card_step = 2
                    auto_save_current_session()
                    st.rerun()
            with col_next:
                if st.button("Next: speech validation ➔", key="next_c3", use_container_width=True, type="primary"):
                    st.session_state.completed_card_steps.add(3)
                    st.session_state.active_card_step = 4
                    st.session_state.speech_eval_result = None
                    auto_save_current_session()
                    st.rerun()

        # -------------------------------------------------------------
        # STAGE 4: SPEECH VALIDATION
        # -------------------------------------------------------------
        elif st.session_state.active_card_step == 4:
            st.markdown("## Voice Practice & Speech Evaluation")

            st.markdown("Speak this sentence aloud:")
            st.markdown(f"<div style='font-size:1.35rem; font-weight:600; color:#174EA6; background-color:#E8F0FE; padding:16px; border-radius:12px; border-left:5px solid #1A73E8;'>{pack.card4_speech.target_phrase}</div>", unsafe_allow_html=True)

            st.markdown(f"*Expected phonetic flow: `{pack.card4_speech.expected_phonetics}`*")
            st.caption(f"Focus sounds: {pack.card4_speech.key_focus_sounds}")

            st.markdown("#### 🎙️ Record or submit your voice:")

            voice_tab1, voice_tab2 = st.tabs(["Microphone recording", "Text transcript confirmation"])

            with voice_tab1:
                try:
                    from streamlit_mic_recorder import mic_recorder
                    audio_record = mic_recorder(
                        start_prompt="🔴 Start recording",
                        stop_prompt="⏹️ Stop recording",
                        key=f"speech_mic_recorder_{current_tense_name}"
                    )
                    if audio_record:
                        st.audio(audio_record['bytes'])
                        transcribed = transcribe_audio_bytes(audio_record['bytes'], lang=st.session_state.current_curriculum.get("target_language_code", "es"))
                        if transcribed:
                            st.write(f"Transcribed speech: **{transcribed}**")
                            if st.button("Evaluate recorded speech", key=f"eval_rec_{current_tense_name}"):
                                log_ve_event("speech_validate_audio", "submit")
                                with st.spinner("LingoCraft AI Speech Validator analyzing phonetics..."):
                                    eval_res = orchestrator.validate_speech(
                                        spoken_text=transcribed,
                                        target_phrase=pack.card4_speech.target_phrase,
                                        target_lang=target_l,
                                        native_lang=native_l
                                    )
                                    st.session_state.speech_eval_result = eval_res
                        else:
                            st.warning("Speech could not be transcribed cleanly from recording. You can also confirm your speech in the text tab.")
                except Exception as e:
                    st.info("Microphone input ready. You can also validate your pronunciation in the text tab.")

            with voice_tab2:
                spoken_input = st.text_input("Type or confirm what you said:", value=pack.card4_speech.target_phrase, key=f"text_speech_{current_tense_name}")
                if st.button("Evaluate pronunciation", key=f"eval_text_{current_tense_name}"):
                    log_ve_event("speech_validate_text", "submit")
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
                if score >= 75:
                    award_xp(25, f"speech_verified_{current_tense_name}", "Speech pronunciation accuracy (75%+)")
                else:
                    award_xp(10, f"speech_attempt_{current_tense_name}", "Voice practice vocalization effort")

                st.markdown("### Evaluation feedback:")
                st.progress(score / 100)
                st.write(f"**Accuracy score:** {score}%")

                # Word-level visual diff chips
                if res.get("diff_html"):
                    st.markdown(res["diff_html"], unsafe_allow_html=True)

                if score >= 75:
                    st.markdown(f"<div class='feedback-box-success' role='status' aria-live='polite'><h4>{res.get('feedback_title', '¡Excelente!')}</h4><p>{res.get('evaluation_message')}</p><p><strong>Tip:</strong> {res.get('actionable_tip')}</p></div>", unsafe_allow_html=True)
                else:
                    st.session_state.needs_review_tenses.add(st.session_state.active_tense_index)
                    st.markdown(f"<div class='feedback-box-error' role='alert' aria-live='assertive'><h4>{res.get('feedback_title', 'Constructive feedback')}</h4><p>{res.get('evaluation_message')}</p><p><strong>Adjustment:</strong> {res.get('actionable_tip')}</p></div>", unsafe_allow_html=True)
                    st.markdown("<p style='font-size:0.8125rem; color:#B06000; margin-top:6px;'>🔄 <em>This stage has been automatically flagged as <strong>Needs review</strong> in your roadmap.</em></p>", unsafe_allow_html=True)
                    if res.get("requires_micro_practice") and res.get("micro_practice_drill"):
                        st.warning(f"🔄 **Immediate micro-practice:** {res.get('micro_practice_drill')}")

            render_incontext_coach(current_tense_name, 4, pack, target_l, native_l)

            st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
            col_prev, col_next = st.columns([1.2, 1.4])
            with col_prev:
                if st.button("⬅ Back to pronunciation", key="back_c4", use_container_width=True):
                    st.session_state.active_card_step = 3
                    auto_save_current_session()
                    st.rerun()
            with col_next:
                if st.button("Next: conjugation quiz ➔", key="next_c4", use_container_width=True, type="primary"):
                    st.session_state.completed_card_steps.add(4)
                    st.session_state.active_card_step = 5
                    st.session_state.quiz_eval_result = None
                    st.session_state.micro_practice_result = None
                    auto_save_current_session()
                    st.rerun()

        # -------------------------------------------------------------
        # STAGE 5: CONJUGATION QUIZ (Shuffled Options & No Pre-selection)
        # -------------------------------------------------------------
        elif st.session_state.active_card_step == 5:
            st.markdown("## Master Tense Conjugation Challenge")

            st.markdown("#### Fill in the blank with the correct form:")
            st.markdown(f"<div style='font-size:1.3rem; font-weight:500; color:#202124; background-color:#F8F9FA; padding:18px; border-radius:12px; border:1px solid #DADCE0;'>{pack.card5_quiz.sentence_prompt}</div>", unsafe_allow_html=True)

            # Shuffle options persistently for this tense pack so option A is NOT always correct
            quiz_shuffle_key = f"quiz_shuffled_{current_tense_name}"
            if quiz_shuffle_key not in st.session_state:
                opts = list(pack.card5_quiz.options)
                random.seed(len(current_tense_name) * 42)
                random.shuffle(opts)
                st.session_state[quiz_shuffle_key] = opts

            display_options = st.session_state[quiz_shuffle_key]

            # index=None forces user to actively pick an option (no spoilers)
            quiz_choice = st.radio(
                "Choose the correct answer:",
                display_options,
                index=None,
                key=f"quiz_radio_{current_tense_name}"
            )

            col_submit, col_skip_t = st.columns([2, 1])
            with col_submit:
                if st.button("Submit answer 🚀", type="primary", use_container_width=True):
                    if quiz_choice is None:
                        st.warning("⚠️ Select an answer before submitting.")
                    else:
                        log_ve_event("quiz_submit", "submit", {"choice": quiz_choice})
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
                if st.button("⏩ Skip and mark tense complete", key="skip_quiz", use_container_width=True):
                    st.session_state.completed_card_steps.add(5)
                    st.session_state.completed_tenses.add(st.session_state.active_tense_index)
                    st.session_state.needs_review_tenses.discard(st.session_state.active_tense_index)
                    st.session_state.active_tense_index += 1
                    st.session_state.active_card_step = 1
                    st.session_state.completed_card_steps = set()
                    st.session_state.current_pack = None
                    st.session_state.speech_eval_result = None
                    st.session_state.quiz_eval_result = None
                    auto_save_current_session()
                    st.rerun()

            # Display Quiz Feedback
            if st.session_state.quiz_eval_result:
                qres = st.session_state.quiz_eval_result
                if qres["is_correct"]:
                    award_xp(20, f"quiz_solved_{current_tense_name}", "Conjugation challenge passed")
                    st.session_state.completed_card_steps.add(5)
                    st.session_state.needs_review_tenses.discard(st.session_state.active_tense_index)
                    st.markdown(f"<div class='feedback-box-success' role='status' aria-live='polite'><h3>{qres.get('headline')}</h3><p>{qres.get('feedback')}</p></div>", unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)

                    # Advance to Next Tense Button
                    if st.button("🏆 Complete tense and advance to next ➔", type="primary", use_container_width=True):
                        award_xp(50, f"stage_mastered_{current_tense_name}", f"Stage mastered: {current_tense_name}")
                        st.session_state.completed_tenses.add(st.session_state.active_tense_index)
                        st.session_state.needs_review_tenses.discard(st.session_state.active_tense_index)
                        st.session_state.active_tense_index += 1
                        st.session_state.active_card_step = 1
                        st.session_state.completed_card_steps = set()
                        st.session_state.current_pack = None
                        st.session_state.speech_eval_result = None
                        st.session_state.quiz_eval_result = None
                        auto_save_current_session()
                        st.rerun()

                else:
                    st.session_state.needs_review_tenses.add(st.session_state.active_tense_index)
                    st.markdown(f"<div class='feedback-box-error' role='alert' aria-live='assertive'><h3>{qres.get('headline')}</h3><p>{qres.get('feedback')}</p><p><strong>Why this mistake is common:</strong> {qres.get('why_common_mistake')}</p></div>", unsafe_allow_html=True)
                    st.markdown("<p style='font-size:0.8125rem; color:#B06000; margin-top:6px;'>🔄 <em>This tense has been flagged as <strong>Needs review</strong> in your roadmap.</em></p>", unsafe_allow_html=True)

                    # Immediate Micro-Practice Drill
                    if qres.get("micro_practice_prompt"):
                        st.markdown("---")
                        st.markdown("### 🛠️ Immediate micro-practice drill")
                        st.markdown(f"**{qres.get('micro_practice_prompt')}**")
                        mp_options = qres.get("micro_practice_options", [])
                        if mp_options:
                            user_mp_choice = st.radio("Select the micro-practice answer:", mp_options, index=None, key=f"mp_radio_{current_tense_name}")
                            if st.button("Verify micro-practice"):
                                if user_mp_choice is None:
                                    st.warning("⚠️ Select an option first.")
                                else:
                                    correct_mp_idx = qres.get("micro_practice_correct_index", 0)
                                    if 0 <= correct_mp_idx < len(mp_options) and user_mp_choice == mp_options[correct_mp_idx]:
                                        st.success(f"¡Bien hecho! {qres.get('micro_practice_explanation')}")
                                        st.session_state.micro_practice_result = True
                                        award_xp(15, f"resilience_{current_tense_name}", "Resilience bonus: Review drill cleared")
                                    else:
                                        st.error("Not quite yet. Remember the core rule and try once more.")

                        if st.session_state.micro_practice_result:
                            if st.button("Now advance to next tense ➔", type="primary"):
                                award_xp(50, f"stage_mastered_{current_tense_name}", f"Stage mastered: {current_tense_name}")
                                st.session_state.completed_card_steps.add(5)
                                st.session_state.completed_tenses.add(st.session_state.active_tense_index)
                                st.session_state.needs_review_tenses.discard(st.session_state.active_tense_index)
                                st.session_state.active_tense_index += 1
                                st.session_state.active_card_step = 1
                                st.session_state.completed_card_steps = set()
                                st.session_state.current_pack = None
                                st.session_state.speech_eval_result = None
                                st.session_state.quiz_eval_result = None
                                auto_save_current_session()
                                st.rerun()

            render_incontext_coach(current_tense_name, 5, pack, target_l, native_l)

            st.markdown("<hr style='margin:24px 0 16px 0;'>", unsafe_allow_html=True)
            col_prev, col_space = st.columns([1.2, 4])
            with col_prev:
                if st.button("⬅ Back to speech validation", key="back_c5", use_container_width=True):
                    st.session_state.active_card_step = 4
                    auto_save_current_session()
                    st.rerun()


# Persist current session snapshot to SQLite
auto_save_current_session()

