import streamlit as st
import random
import io
import json
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
from pydantic import BaseModel, Field

import ai_marking_component

class AIWorksheetSolutions(BaseModel):
    solutions: list[str]

# --- Science Engine: MOTION & FORCES ---
def generate_forces_problem(level="1", quiz_style="Both"):
    # Pool 1: Multiple Choice Concepts
    mcq_pool = [
        {"q": "A force is best described as:", "ans": "A push or a pull", "distractors": ["Energy stored in an object", "Matter moving through space", "Mass × speed"]},
        {"q": "Which of the following is a non-contact force?", "ans": "Gravity", "distractors": ["Friction", "Air resistance", "Upthrust"]},
        {"q": "Force is measured in:", "ans": "Newtons", "distractors": ["Kilograms", "Metres", "Seconds"]},
        {"q": "Which statement best describes Newton's First Law?", "ans": "Objects resist changes in motion", "distractors": ["F = ma", "Every action has an equal and opposite reaction", "Pressure increases with depth"]},
        {"q": "Balanced forces produce:", "ans": "A net force of zero", "distractors": ["Acceleration", "Increasing speed", "Motion in a circle"]},
        {"q": "Which force opposes motion through air?", "ans": "Air resistance", "distractors": ["Gravity", "Upthrust", "Magnetism"]},
        {"q": "The standard unit of mass is:", "ans": "Kilogram", "distractors": ["Newton", "Metre", "Joule"]},
        {"q": "A vector quantity has:", "ans": "Size and direction", "distractors": ["Size only", "Direction only", "Mass and weight"]},
        {"q": "Atmospheric pressure:", "ans": "Decreases with altitude", "distractors": ["Increases with altitude", "Remains constant", "Is always zero"]},
        {"q": "A floating boat experiences:", "ans": "Balanced weight and upthrust", "distractors": ["Weight only", "Upthrust only", "Friction only"]}
    ]

    # Pool 2: Written / Calculation Concepts
    written_pool = [
        {"type": "define", "term": "Velocity", "ans": "Speed in a given direction (vector quantity)."},
        {"type": "define", "term": "Acceleration", "ans": "The rate of change of velocity over time."},
        {"type": "explain", "term": "Difference between mass and weight", "ans": "Mass is the amount of matter (kg), weight is the force of gravity acting on that mass (N)."},
        {"type": "state", "term": "Newton's Third Law", "ans": "For every action force, there is an equal and opposite reaction force."},
        {"type": "calc_net", "context": "A car experiences a driving force of {f1} N forward and friction of {f2} N backward."},
        {"type": "calc_fma", "context": "Calculate the force required to accelerate a {m} kg mass at {a} m/s²."},
        {"type": "calc_fma_mass", "context": "A skateboard is pushed with a force of {f} N and accelerates at {a} m/s². Calculate its mass."}
    ]

    if quiz_style == "Multiple Choice":
        choice = "MCQ"
    elif quiz_style == "Written Answers":
        choice = "Written"
    else:
        choice = random.choice(["MCQ", "Written"])

    if choice == "MCQ":
        item = random.choice(mcq_pool)
        options = item["distractors"] + [item["ans"]]
        random.shuffle(options)
        return {"mode": "MCQ", "text": item["q"], "options": options, "ans": item["ans"]}
    else:
        item = random.choice(written_pool)
        if item["type"] == "define":
            text = f"Define the following term:\n\n{item['term']}"
            return {"mode": "Written", "text": text, "ans": item["ans"]}
        elif item["type"] == "explain" or item["type"] == "state":
            text = f"{item['term']}"
            return {"mode": "Written", "text": text, "ans": item["ans"]}
        elif item["type"] == "calc_net":
            f1, f2 = random.randint(500, 900), random.randint(100, 300)
            text = item["context"].format(f1=f1, f2=f2) + "\n\nCalculate the net force and state its direction."
            ans = f"{f1 - f2} N forward"
            return {"mode": "Written", "text": text, "ans": ans}
        elif item["type"] == "calc_fma":
            m, a = random.randint(2, 12), random.randint(2, 8)
            text = item["context"].format(m=m, a=a)
            ans = f"{m * a} N"
            return {"mode": "Written", "text": text, "ans": ans}
        elif item["type"] == "calc_fma_mass":
            m, a = random.randint(2, 10), random.randint(2, 6)
            f = m * a
            text = item["context"].format(f=f, a=a)
            ans = f"{m} kg"
            return {"mode": "Written", "text": text, "ans": ans}

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

# --- Worksheet PDF Generator ---
def create_pdf_bytes(quiz_style="Both"):
    buffer = io.BytesIO()
    with PdfPages(buffer) as pdf:
        problems = [generate_forces_problem(quiz_style=quiz_style) for _ in range(20)]
        
        fig_ws, axes = plt.subplots(5, 4, figsize=(8.27, 11.69))
        fig_ws.subplots_adjust(left=0.04, right=0.96, top=0.92, bottom=0.04, wspace=0.15, hspace=0.30)
        fig_ws.suptitle("Year 9 Science: Motion & Forces Worksheet", fontsize=16, fontweight='bold', ha='center')
        
        for idx, p_data in enumerate(problems):
            row, col = divmod(idx, 4)
            ax = axes[row, col]
            ax.axis('off')
            txt = f"Q{idx+1}: {p_data['text']}"
            if p_data["mode"] == "MCQ":
                opts = "\n".join([f"- {o}" for o in p_data['options']])
                txt += f"\n{opts}"
            wrapped = "\n".join(textwrap.wrap(txt, width=30))
            ax.text(0, 1, wrapped, fontsize=8, va='top')
            
        pdf.savefig(fig_ws)
        plt.close(fig_ws)

        fig_ans, ax_ans = plt.subplots(figsize=(8.27, 11.69))
        ax_ans.axis('off')
        ax_ans.text(0.5, 0.96, "Answer Key", fontsize=16, fontweight='bold', ha='center')
        for i in range(10):
            left_idx, right_idx = i, i + 10
            txt_l = f"Q{left_idx+1}: {problems[left_idx]['ans']}"
            txt_r = f"Q{right_idx+1}: {problems[right_idx]['ans']}"
            y_pos = 0.90 - (i * 0.088)
            ax_ans.text(0.04, y_pos, "\n".join(textwrap.wrap(txt_l, 45)), fontsize=8, va='top')
            ax_ans.text(0.52, y_pos, "\n".join(textwrap.wrap(txt_r, 45)), fontsize=8, va='top')
        pdf.savefig(fig_ans)
        plt.close(fig_ans)

    buffer.seek(0)
    return buffer.getvalue()

def handle_settings_change():
    st.session_state.generating = True
    st.session_state.pdf_bytes = None
    st.session_state.problem_suite_refresh_id += 1 

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

    if 'generating' not in st.session_state: st.session_state.generating = True
    if 'pdf_bytes' not in st.session_state: st.session_state.pdf_bytes = None
    if 'problem_suite_refresh_id' not in st.session_state: st.session_state.problem_suite_refresh_id = 0
    if 'quiz_style' not in st.session_state: st.session_state.quiz_style = "Both"

    st.title("Motion & Forces Quiz 🚀")

    col_actions, col_set = st.columns([5, 1])
    with col_actions:
        with st.popover("📄 Worksheet Actions", use_container_width=True):
            if st.session_state.pdf_bytes is None:
                if st.button("⚙️ Generate 20-Question PDF", use_container_width=True):
                    with st.spinner("Compiling PDF..."):
                        st.session_state.pdf_bytes = create_pdf_bytes(st.session_state.quiz_style)
                    st.rerun()
            else:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                st.download_button("⬇️ Download Worksheet", data=st.session_state.pdf_bytes, file_name=f"Forces_Motion_{timestamp}.pdf", mime="application/pdf", use_container_width=True, type="primary")

    with col_set:
        with st.popover("⚙️", use_container_width=True):
            st.radio("Quiz Style", ["Multiple Choice", "Written Answers", "Both"], key="quiz_style", on_change=handle_settings_change)
            st.radio("Camera Mode", ["None", "App", "Native"], key="camera_mode", horizontal=True, on_change=handle_settings_change)
            st.toggle("Canvas Controls", key="show_controls", on_change=handle_settings_change)

    if st.session_state.generating:
        with st.spinner("Loading next question..."):
            p_data = generate_forces_problem(quiz_style=st.session_state.quiz_style)
            st.session_state.science_problem_data = p_data
            if p_data["mode"] == "Written":
                st.session_state.problem_image_context = draw_question_image(p_data["text"], width_px=420, height_px=420)
            st.session_state.generating = False
            st.rerun()

    else:
        p_data = st.session_state.science_problem_data
        
        if p_data["mode"] == "MCQ":
            st.write(f"### {p_data['text']}")
            for idx, opt in enumerate(p_data["options"]):
                if st.button(opt, use_container_width=True, key=f"mcq_{idx}_{st.session_state.problem_suite_refresh_id}"):
                    if opt == p_data["ans"]:
                        st.success("✅ Correct!")
                    else:
                        st.error(f"❌ Incorrect. The correct answer is: {p_data['ans']}")
        else:
            bg_image = st.session_state.problem_image_context
            
            # --- The AI no longer receives the 'ans' parameter! It figures it out itself. ---
            problem_context = f"Science Question: {p_data['text']}"
            
            ai_marking_component.render_grading_suite(
                bg_image=bg_image,
                height_px=420,
                key_prefix=f"sci_suite_{st.session_state.problem_suite_refresh_id}",
                solution_requirement="general",
                problem_context=problem_context,
                show_controls=st.session_state.get('show_controls', False),
                camera_mode=st.session_state.get('camera_mode', 'App')
            )

        st.markdown('<div id="next-problem-btn"></div>', unsafe_allow_html=True)
        if st.button("Next Question", use_container_width=True):
            handle_settings_change()
            st.rerun()