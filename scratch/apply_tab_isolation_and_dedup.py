import re

with open("app.py", "r") as f:
    code = f.read()

# 1. Update datetime import to include timedelta
old_dt = "from datetime import datetime"
new_dt = "from datetime import datetime, timedelta"
assert old_dt in code, "Could not find old_dt"
code = code.replace(old_dt, new_dt, 1)

# 2. Add Deploy button & header hiding CSS
old_css_ring = "/* Accessibility focus rings */"
new_css_hide = """    /* Hide default Streamlit header and Deploy watermark */
    .stAppHeader, .stDeployButton, header[data-testid="stHeader"] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
    }

    /* Style top main navigation segmented control */
    div[data-testid="stSegmentedControl"] {
        margin: 12px 0 16px 0;
        display: flex;
        justify-content: center;
    }
    div[data-testid="stSegmentedControl"] button {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 6px 18px !important;
        border-radius: 9999px !important;
    }

    /* Accessibility focus rings */"""
assert old_css_ring in code, "Could not find old_css_ring"
code = code.replace(old_css_ring, new_css_hide, 1)

# 3. Add format_relative_timestamp helper function
helper_search = "def safe_set_main_tab(tab_name: str):"
helper_func = """def format_relative_timestamp(ts: float) -> str:
    \"\"\"Formats a UNIX timestamp into a human-friendly relative time string.\"\"\"
    try:
        dt = datetime.fromtimestamp(ts)
        now = datetime.now()
        if dt.date() == now.date():
            return f"Today, {dt.strftime('%I:%M %p').lstrip('0')}"
        elif dt.date() == (now.date() - timedelta(days=1)):
            return f"Yesterday, {dt.strftime('%I:%M %p').lstrip('0')}"
        else:
            return dt.strftime("%b %d, %I:%M %p")
    except Exception:
        return time.strftime("%b %d, %H:%M", time.localtime(ts))


def safe_set_main_tab(tab_name: str):
    \"\"\"Safely updates main_tab, or queues it if widget is already instantiated.\"\"\"
    st.session_state.main_tab = tab_name
    st.session_state["_pending_main_tab"] = tab_name
    st.session_state["main_tab_control"] = tab_name
"""
assert helper_search in code, "Could not find helper_search"
code = code.replace(helper_search + """
    \"\"\"Safely updates main_tab, or queues it if widget is already instantiated.\"\"\"
    try:
        st.session_state.main_tab = tab_name
    except (StreamlitWidgetAlreadyInstantiatedError, Exception):
        st.session_state["_pending_main_tab"] = tab_name""", helper_func, 1)

# 4. Update sidebar recent sessions deduplication and relative timestamps
old_recents = """        recents = session_manager.list_recent_sessions(limit=5)
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
                if st.button(f"▶️ {c_lbl}", key=f"rec_btn_{r['session_id']}", help=f"Code: {r['session_id']} | Updated: {t_str}", use_container_width=True):"""

new_recents = """        recents = session_manager.list_recent_sessions(limit=5, dedup_by_topic=True)
        other_recents = [r for r in recents if r["session_id"] != st.session_state.session_id]
        if other_recents:
            st.markdown("##### 🕒 Recent Study Sessions:")
            for r in other_recents:
                t_str = format_relative_timestamp(r["updated_at"])
                rev_n = r.get("needs_review_count", 0)
                rev_suffix = f" | 🔄 {rev_n}" if rev_n > 0 else ""
                xp_n = r.get("xp_points", 0)
                xp_suffix = f" | ⚡ {xp_n} XP" if xp_n > 0 else ""
                raw_topic = r['topic']
                if "—" in raw_topic:
                    display_topic = raw_topic.split("—")[-1].strip()
                elif ":" in raw_topic:
                    display_topic = raw_topic.split(":")[-1].strip()
                else:
                    display_topic = raw_topic[:18]
                c_lbl = f"{display_topic} (🏆 {r['completed_count']}/{r['total_tenses']}{xp_suffix})"
                st.caption(f"📅 *{t_str}*")
                if st.button(f"▶️ {c_lbl}", key=f"rec_btn_{r['session_id']}", help=f"Code: {r['session_id']} | Updated: {t_str}", use_container_width=True):"""

assert old_recents in code, "Could not find old_recents"
code = code.replace(old_recents, new_recents, 1)

# 5. Header popover "ℹ️" -> "About"
old_popover = 'with st.popover("ℹ️", use_container_width=True, help="About LingoCraft AI"):'
new_popover = 'with st.popover("About", use_container_width=True, help="About LingoCraft AI"):'
assert old_popover in code, "Could not find old_popover"
code = code.replace(old_popover, new_popover, 1)

# 6. Replace st.tabs with strictly isolated st.segmented_control
# Find the tabs definition block
old_tabs_block = """if "_pending_main_tab" in st.session_state:
    st.session_state.main_tab = st.session_state.pop("_pending_main_tab")

# Main Navigation Tabs
tab_learn, tab_coach, tab_curriculum = st.tabs(
    MAIN_TAB_OPTIONS,
    key="main_tab",
    on_change="rerun"
)

with tab_curriculum:"""

new_tabs_block = """if "_pending_main_tab" in st.session_state:
    st.session_state.main_tab = st.session_state.pop("_pending_main_tab")
    st.session_state["main_tab_control"] = st.session_state.main_tab

# Main Navigation Tabs (Strictly Isolated Views)
selected_tab = st.segmented_control(
    "Navigation View",
    options=MAIN_TAB_OPTIONS,
    default=st.session_state.get("main_tab", MAIN_TAB_LEARN),
    key="main_tab_control",
    label_visibility="collapsed"
)
if not selected_tab:
    selected_tab = st.session_state.get("main_tab", MAIN_TAB_LEARN)
st.session_state.main_tab = selected_tab

sync_url_params()

if selected_tab == MAIN_TAB_CURRICULUM:"""

assert old_tabs_block in code, "Could not find old_tabs_block"
code = code.replace(old_tabs_block, new_tabs_block, 1)

# Replace "with tab_coach:" with "elif selected_tab == MAIN_TAB_COACH:"
old_coach_block = "with tab_coach:"
new_coach_block = "elif selected_tab == MAIN_TAB_COACH:"
assert old_coach_block in code, "Could not find old_coach_block"
code = code.replace(old_coach_block, new_coach_block, 1)

# Replace "with tab_learn:" with "else:"
old_learn_block = "with tab_learn:"
new_learn_block = "else:"
assert old_learn_block in code, "Could not find old_learn_block"
code = code.replace(old_learn_block, new_learn_block, 1)

# 7. Disambiguate top skip button in tab_learn
old_skip_btn = 'if st.button("🏆 Mark mastered ➔", help="Jump to the next stage if you already know this form", use_container_width=True):'
new_skip_btn = 'if st.button("✓ Skip to next stage ➔", help="Jump to the next stage if you already know this form", use_container_width=True):'
assert old_skip_btn in code, "Could not find old_skip_btn"
code = code.replace(old_skip_btn, new_skip_btn, 1)

with open("app.py", "w") as f:
    f.write(code)

print("Tab isolation and deduplication applied successfully!")
