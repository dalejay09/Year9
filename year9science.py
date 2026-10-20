import streamlit as st

# 1. Page Config MUST be the first Streamlit command
st.set_page_config(page_title="Year 9 Science Revision", page_icon="🔬", layout="centered")

# 2. Import your science modules
import forcesandmotion_year9_module as forces_motion

# 3. Create a tab-reset handler
def handle_nav_change():
    st.session_state.generating = True 
    st.session_state.pdf_bytes = None
    st.session_state.id_feedback = ""

# 4. Clean Tab Navigation
st.markdown("""
    <style>
    div[role="radiogroup"] {
        justify-content: center;
        gap: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

selected_app = st.radio(
    "Navigation", 
    ["Motion & Forces", "Energy", "Chemistry Basics", "Biology"],
    horizontal=True,
    label_visibility="collapsed",
    on_change=handle_nav_change
)

st.markdown("<hr style='margin: 0.2em 0px 1.5em 0px; border-color: #444;'>", unsafe_allow_html=True)

# 5. Route to the correct app
if selected_app == "Motion & Forces":
    forces_motion.run_app()
elif selected_app == "Energy":
    st.info("⚡ Energy module is under construction.")
elif selected_app == "Chemistry Basics":
    st.info("🧪 Chemistry module is under construction.")
elif selected_app == "Biology":
    st.info("🧬 Biology module is under construction.")