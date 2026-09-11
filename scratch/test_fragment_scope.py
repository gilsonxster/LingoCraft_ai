import streamlit as st

st.title("Fragment Test")

if "count" not in st.session_state:
    st.session_state.count = 0

st.write(f"Outer count: {st.session_state.count}")

if st.button("Increment Outer"):
    st.session_state.count += 1
    st.rerun()

@st.fragment
def my_fragment():
    st.write("Inside Fragment")
    if st.button("Rerun Fragment"):
        st.rerun() # Should rerun only fragment?
    
    if st.button("Rerun App"):
        st.rerun(scope="app") # Should rerun whole app?

my_fragment()
