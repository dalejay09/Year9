import streamlit as st
import random
import io
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image

import ai_marking_component

# --- Math Engine: SYSTEMS OF EQUATIONS ---
def get_all_problems():
    written_pool = [
        {"class": 3, "type": "solve", "term": "Solve the system:\n2y = 2\n-2g + 2y - 3z = -15\n2g + y + 2z = 15", "ans": "g = 4, y = 1, z = 3"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n-d - x = -4\nd + 3m + 2x = 12\n-d - 2m - 3x = -12", "ans": "d = 2, m = 2, x = 2"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n-n + 2w + 3y = 10\nn + 2w - 3y = 2\nn + 2w + y = 6", "ans": "n = -1, w = 3, y = 1"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n3m + 3n - 3y = 0\n2m - 2n - y = 5\nm - 2n + y = 0", "ans": "m = -1, n = -2, y = -3"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n-2h - 2k = 6\n3(-d - 2h + 2k) = -33\n3d + 2h - 2k = 13", "ans": "d = 1, h = 1, k = -4"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n3n = 3\n-n - 3x = -10\n-3n - 3t = 3", "ans": "n = 1, t = -2, x = 3"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n-3m + n = -6\n3(3m + 3n + 2x) = 42\n2(-m - 2n - 3x) = -6", "ans": "m = 3, n = 3, x = -2"},
        {"class": 3, "type": "solve", "term": "Solve the system:\nm - n + z = 4\n-m - 2n + 2z = 14\n-2n + 3z = 15", "ans": "m = -2, n = -3, z = 3"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n3h + p = -10\n2h - p + 2w = 4\n2h - 3p - w = 6", "ans": "h = -2, p = -4, w = 2"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n-3u = -6\n-3a + 2u - 3w = -2\n3a + 2u - w = 18", "ans": "a = 4, u = 2, w = -2"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n-3p + 3r = 6\n-3d + 2p = 16\n3d - p + 3r = -2", "ans": "d = -4, p = 2, r = 4"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n-2c - j = -8\n2c - 2j + 3k = -7\n-2c + j + 3k = -13", "ans": "c = 3, j = 2, k = -3"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n2m - 2r + 2t = -14\n-2m - 3r + t = -8\n-3m - 3r - 2t = 5", "ans": "m = -1, r = 2, t = -4"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n-3m - 3q = 24\nm + 2q = -12\n-3g - 2m + 2q = -9", "ans": "g = 3, m = -4, q = -4"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n-t - v + z = 2\n3t - v - z = 10\n-t + 2v - 3z = -15", "ans": "t = 3, v = -3, z = 2"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n2c + x = -4\n2c - 3x = -12\n-2c + 2x - 2y = 16", "ans": "c = -3, x = 2, y = -3"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n2s = 6\n3h = 6\n-2h - 3s + 2t = -15", "ans": "h = 2, s = 3, t = -1"},
        {"class": 3, "type": "solve", "term": "Solve the system:\nd - 3x = 7\n-2d + 3n + 3x = -11\n3d - 3n = 6", "ans": "d = 1, n = -1, x = -2"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n3m + 3x = -6\n3m + 2w - 3x = 22\n3m + w - 2x = 16", "ans": "m = 2, w = 2, x = -4"},
        {"class": 3, "type": "solve", "term": "Solve the system:\n-2a - v = 1\n2a - 2r - 2v = -16\n3a - 3r - v = -18", "ans": "a = -2, r = 3, v = 3"}
    ]
    return [], written_pool

def get_next_question():
    mode = st.session_state.get('selection_mode', 'Random')
    
    if mode == "Random":
        _, written_pool = get_all_problems()
        raw_item = random.choice(written_pool).copy()
    else:
        if 'math_question_queue' not in st.session_state or not st.session_state.math_question_queue:
            if mode == "Quiz":
                st.session_state.math_quiz_score = 0
                st.session_state.math_questions_answered = 0
                st.session_state.math_quiz_completed = False
                
            _, combined_pool = get_all_problems()
            random.shuffle(combined_pool)
            
            if mode == "Quiz" and len(combined_pool) > 20:
                combined_pool = combined_pool[:20]
                
            st.session_state.math_question_queue = combined_pool
            
        if mode == "Quiz" and not st.session_state.math_question_queue:
            st.session_state.math_quiz_completed = True
            return None
            
        raw_item = st.session_state.math_question_queue.pop(0)

    raw_item["mode"] = "Written"
    raw_item["text"] = raw_item["term"]
    rule = f"The student must show working to solve the simultaneous equations. The final correct variables are: {raw_item['ans']}"
    raw_item["grading_rule"] = rule
    raw_item["options"] = []
    
    return raw_item

# --- Visual Engine ---
def draw_question_image(text, width_px=420, height_px=760):
    fig, ax = plt.subplots(figsize=(width_px/100, height_px/100), dpi=100)
    fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    wrapped_text = "\n".join(textwrap.wrap(text, width=40))
    ax.text(0.02, 0.98, wrapped_text, fontsize=13, ha='left', va='top', wrap=True, family='sans-serif', color='black')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, facecolor='white', transparent=False)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert('RGBA').copy()

def handle_settings_change():
    st.session_state.math_generating = True
    st.session_state.math_problem_suite_refresh_id += 1 
    st.session_state.math_question_queue = []
    st.session_state.math_quiz_active = False
    st.session_state.math_quiz_score = 0
    st.session_state.math_questions_answered = 0
    st.session_state.math_quiz_completed = False

# --- START OF MODULE WRAPPER ---
def run_app():
    st.markdown("""
        <style>
        button[kind="primary"] { background-color: #007AFF !important; border-color: #007AFF !important; color: white !important; }
        button[kind="primary"]:hover { background-color: #0056b3 !important; border-color: #0056b3 !important; }
        div[data-testid="stElementContainer"]:has(#next-problem-btn) + div[data-testid="stElementContainer"] button {
            background-color: #28a745 !important; border-color: #28a745 !important; color: white !important;
        }
        div[data-testid="stElementContainer"]:has(#next-problem-btn) + div[data-testid="stElementContainer"] button:hover {
            background-color: #218838 !important; border-color: #218838 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # State Initializations
    if 'math_generating' not in st.session_state: st.session_state.math_generating = True
    if 'math_problem_suite_refresh_id' not in st.session_state: st.session_state.math_problem_suite_refresh_id = 0
    if 'selection_mode' not in st.session_state: st.session_state.selection_mode = "Random"
    if 'math_quiz_active' not in st.session_state: st.session_state.math_quiz_active = False
    if 'math_questions_answered' not in st.session_state: st.session_state.math_questions_answered = 0

    st.title("Systems of Equations 🧮")

    col_actions, col_set = st.columns([4, 1])
    with col_set:
        with st.popover("⚙️", use_container_width=True):
            st.radio("Selection Mode", ["Random", "Cyclical", "Rehearse", "Quiz"], key="selection_mode", on_change=handle_settings_change)
            st.radio("Camera Mode", ["None", "App", "Native"], key="camera_mode", horizontal=True, on_change=handle_settings_change)
            st.toggle("Canvas Controls", key="show_controls", on_change=handle_settings_change)

    # --- START SCREEN GATE ---
    if st.session_state.selection_mode == "Quiz" and not st.session_state.math_quiz_active:
        if st.session_state.get('math_quiz_completed', False):
            st.success(f"🎉 Quiz Complete! You scored {st.session_state.math_quiz_score} out of {st.session_state.math_questions_answered}.")
            if st.button("Restart Quiz"):
                handle_settings_change()
                st.rerun()
            return
            
        st.info("Ready to test your knowledge? This quiz will generate random questions based on your style settings.")
        if st.button("🚀 Start Quiz", use_container_width=True, type="primary"):
            st.session_state.math_quiz_active = True
            st.session_state.math_quiz_score = 0
            st.session_state.math_questions_answered = 0
            st.rerun()
        return

    # --- RUNNING SCORE DASHBOARD ---
    if st.session_state.selection_mode == "Quiz" and st.session_state.math_quiz_active:
        col1, col2, col3 = st.columns(3)
        col1.metric("Score", f"{st.session_state.math_quiz_score}")
        col2.metric("Question", f"{st.session_state.math_questions_answered + 1} / 20")
        acc = int((st.session_state.math_quiz_score / max(1, st.session_state.math_questions_answered)) * 100) if st.session_state.math_questions_answered > 0 else 0
        col3.metric("Accuracy", f"{acc}%")
        st.divider()

    if st.session_state.math_generating or 'math_problem_data' not in st.session_state:
        st.session_state.math_generating = True
        with st.spinner("Loading next question..."):
            p_data = get_next_question()
            if p_data is None: 
                st.session_state.math_quiz_active = False 
                st.rerun() 
                
            st.session_state.math_problem_data = p_data
            st.session_state.problem_image_context = draw_question_image(p_data["text"], width_px=420, height_px=420)
            st.session_state.math_generating = False
            st.rerun()

    else:
        p_data = st.session_state.math_problem_data
        bg_image = st.session_state.problem_image_context
        problem_context = f"Question: {p_data['text']}\nGrading Rule: {p_data.get('grading_rule', '')}"
        
        ai_marking_component.render_grading_suite(
            bg_image=bg_image,
            height_px=420,
            key_prefix=f"math_suite_{st.session_state.math_problem_suite_refresh_id}",
            solution_requirement="general",
            problem_context=problem_context,
            show_controls=st.session_state.get('show_controls', False),
            camera_mode=st.session_state.get('camera_mode', 'App')
        )

        st.markdown('<div id="next-problem-btn"></div>', unsafe_allow_html=True)
        if st.button("Next Question", use_container_width=True):
            if st.session_state.selection_mode == "Cyclical":
                st.session_state.math_question_queue.append(p_data)
            st.session_state.math_generating = True
            st.session_state.math_problem_suite_refresh_id += 1 
            st.rerun()