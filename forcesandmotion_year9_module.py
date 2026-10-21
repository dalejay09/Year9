import streamlit as st
import random
import io
import textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from datetime import datetime
from matplotlib.backends.backend_pdf import PdfPages
from pydantic import BaseModel

import ai_marking_component

# --- Science Engine: MOTION & FORCES ---
def get_all_problems():
    # Pool 1: Multiple Choice Concepts (Class 1) - 30 Questions
    mcq_pool = [
        {"class": 1, "mode": "MCQ", "q": "A force is best described as:", "ans": "A push or a pull", "distractors": ["Energy stored in an object", "Matter moving through space", "Mass × speed"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "Which of the following is a non-contact force?", "ans": "Gravity", "distractors": ["Friction", "Air resistance", "Upthrust"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "Force is measured in:", "ans": "Newtons", "distractors": ["Kilograms", "Metres", "Seconds"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "Which statement best describes Newton's First Law?", "ans": "Objects resist changes in motion", "distractors": ["F = ma", "Every action has an equal and opposite reaction", "Pressure increases with depth"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "Balanced forces produce:", "ans": "A net force of zero", "distractors": ["Acceleration", "Increasing speed", "Motion in a circle"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "Which force opposes motion through air?", "ans": "Air resistance", "distractors": ["Gravity", "Upthrust", "Magnetism"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "The standard unit of mass is:", "ans": "Kilogram", "distractors": ["Newton", "Metre", "Joule"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "A vector quantity has:", "ans": "Size and direction", "distractors": ["Size only", "Direction only", "Mass and weight"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "Atmospheric pressure:", "ans": "Decreases with altitude", "distractors": ["Increases with altitude", "Remains constant", "Is always zero"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "A floating boat experiences:", "ans": "Balanced weight and upthrust", "distractors": ["Weight only", "Upthrust only", "Friction only"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "What is the standard scientific unit for acceleration?", "ans": "m/s²", "distractors": ["m/s", "N", "kg/m"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "Which of the following is an example of a contact force?", "ans": "Friction", "distractors": ["Magnetic force", "Gravitational force", "Electrostatic force"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "A box is pushed with 50 N to the right and pulled with 20 N to the left. What is the net force?", "ans": "30 N to the right", "distractors": ["70 N to the right", "30 N to the left", "70 N to the left"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "What is inertia?", "ans": "The tendency of an object to resist changes in its motion", "distractors": ["A force that slows objects down", "The speed of a falling object", "The weight of an object on Earth"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "Which of these is a scalar quantity (has size, but no direction)?", "ans": "Speed", "distractors": ["Velocity", "Force", "Acceleration"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "What happens to an astronaut's mass and weight if they travel to the Moon?", "ans": "Mass stays the same, weight decreases", "distractors": ["Both mass and weight decrease", "Mass decreases, weight stays the same", "Both mass and weight stay the same"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "If a rock has a mass of 10 kg, what is its approximate weight on Earth? (Assuming g = 10 N/kg)", "ans": "100 N", "distractors": ["10 N", "1 N", "1000 N"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "A 4 kg trolley accelerates at 2 m/s². What is the net force acting on it?", "ans": "8 N", "distractors": ["6 N", "2 N", "16 N"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "When a falling skydiver's air resistance exactly equals their weight downward, they will:", "ans": "Fall at a constant terminal velocity", "distractors": ["Stop moving mid-air", "Accelerate faster towards the ground", "Float upwards"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "The upward force exerted by a solid surface (like a desk) on an object resting on it is called the:", "ans": "Support or Normal force", "distractors": ["Tension force", "Applied force", "Gravitational force"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "Which design feature helps reduce air resistance on a race car?", "ans": "Aerodynamic streamlining", "distractors": ["Increased mass", "Larger surface area", "Rougher paint texture"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "Deceleration is best described as:", "ans": "Negative acceleration (slowing down)", "distractors": ["Moving backward", "Constant speed", "Zero net force"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "If you hit a tennis ball with a racket using 50 N of force, the ball hits the racket with:", "ans": "Exactly 50 N of force", "distractors": ["Less than 50 N of force", "More than 50 N of force", "0 N of force"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "Unbalanced forces acting on an object will ALWAYS cause it to:", "ans": "Change its speed or direction", "distractors": ["Remain completely stationary", "Move at a constant velocity", "Increase its mass"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "On a distance-time graph, a horizontal flat line means the object is:", "ans": "Stationary (not moving)", "distractors": ["Accelerating", "Moving at constant speed", "Decelerating"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "A runner covers 100 meters in 10 seconds. What is their average speed?", "ans": "10 m/s", "distractors": ["1000 m/s", "90 m/s", "1 m/s"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "The gravitational force between two objects depends mostly on their:", "ans": "Mass and distance apart", "distractors": ["Volume and temperature", "Shape and speed", "Air resistance and weight"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "The pulling force transmitted through a stretched rope, string, or cable is called:", "ans": "Tension", "distractors": ["Compression", "Thrust", "Normal force"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "In which of the following situations is friction most helpful?", "ans": "Car tires gripping the road", "distractors": ["Gears grinding in an engine", "Air pushing against an airplane", "A sled sliding down a snowy hill"], "grading_rule": "Exact match multiple choice."},
        {"class": 1, "mode": "MCQ", "q": "A moving object with zero net force acting upon it will:", "ans": "Keep moving at the exact same speed and direction", "distractors": ["Slow down and eventually stop", "Constantly accelerate", "Fall to the ground immediately"], "grading_rule": "Exact match multiple choice."}
    ]

    # Pool 2: Written / Calculation Concepts - 17 Questions
    written_pool = [
        {"class": 3, "type": "define", "term": "Velocity", "ans": "Speed in a given direction (vector quantity)."},
        {"class": 3, "type": "define", "term": "Acceleration", "ans": "The rate of change of velocity over time."},
        {"class": 3, "type": "explain", "term": "Explain the difference between mass and weight.", "ans": "Mass is the amount of matter (kg), weight is the force of gravity acting on that mass (N)."},
        {"class": 3, "type": "state", "term": "State Newton's Third Law.", "ans": "For every action force, there is an equal and opposite reaction force."},
        {"class": 3, "type": "define", "term": "Friction", "ans": "A contact force that opposes motion between two surfaces."},
        {"class": 3, "type": "define", "term": "Net Force", "ans": "The overall or total force acting on an object when all individual forces are combined."},
        {"class": 3, "type": "state", "term": "State Newton's First Law.", "ans": "An object will remain at rest or move at a constant speed in a straight line unless acted upon by an unbalanced force."},
        {"class": 3, "type": "state", "term": "State Newton's Second Law.", "ans": "Force equals mass multiplied by acceleration (F = ma)."},
        {"class": 3, "type": "explain", "term": "What happens to a moving car if the forward engine force and the backward friction force are exactly equal (balanced)?", "ans": "The car will continue moving at a constant speed (zero acceleration)."},
        {"class": 3, "type": "explain", "term": "Explain how action and reaction forces allow a rocket to lift off the ground.", "ans": "The rocket pushes exhaust gases downwards (action), and the gases push the rocket upwards with an equal and opposite force (reaction)."},
        {"class": 3, "type": "explain", "term": "A book rests on a table. Name the downward force and the upward support force acting on it.", "ans": "Downward force: Gravity (or Weight). Upward force: Normal force (or Support force)."},
        {"class": 4, "type": "calc_net", "context": "A car experiences a driving force of {f1} N forward and friction of {f2} N backward."},
        {"class": 4, "type": "calc_fma", "context": "Calculate the force required to accelerate a {m} kg mass at {a} m/s²."},
        {"class": 4, "type": "calc_fma_mass", "context": "A skateboard is pushed with a force of {f} N and accelerates at {a} m/s². Calculate its mass."},
        {"class": 4, "type": "calc_fma_accel", "context": "A force of {f} N is applied to a {m} kg box. Calculate its acceleration."},
        {"class": 4, "type": "calc_weight", "context": "Calculate the weight of a {m} kg object on Earth. (Assume gravity g = 10 N/kg)."},
        {"class": 4, "type": "calc_net_accel", "context": "A boat's engine provides a forward force of {f1} N, and water resistance pulls backward with {f1} N. What is the net force, and will the boat accelerate?"}
    ]
    
    return mcq_pool, written_pool

def generate_forces_problem(quiz_style="Both"):
    mcq_pool, written_pool = get_all_problems()

    if quiz_style == "Multiple Choice":
        choice = "MCQ"
    elif quiz_style == "Written Answers":
        choice = "Written"
    else:
        choice = random.choice(["MCQ", "Written"])

    if choice == "MCQ":
        item = random.choice(mcq_pool).copy()
        options = item["distractors"] + [item["ans"]]
        random.shuffle(options)
        item["options"] = options
        item["text"] = item["q"]
        return item
    else:
        item = random.choice(written_pool).copy()
        item["mode"] = "Written" # Safety tag to prevent KeyError crashes!
        
        if item["class"] == 3:
            if item["type"] == "define":
                text = f"Define the following term:\n\n{item['term']}"
            else:
                text = f"{item['term']}"
            rule = f"The student must articulate the core concept. Exact wording is not required. Core concept: {item['ans']}"
            item.update({"text": text, "options": [], "grading_rule": rule})
            return item
            
        elif item["class"] == 4:
            if item["type"] == "calc_net":
                f1, f2 = random.randint(500, 900), random.randint(100, 300)
                text = item["context"].format(f1=f1, f2=f2) + "\n\nCalculate the net force and state its direction."
                ans = f"{f1 - f2} N forward"
            elif item["type"] == "calc_fma":
                m, a = random.randint(2, 12), random.randint(2, 8)
                text = item["context"].format(m=m, a=a)
                ans = f"{m * a} N"
            elif item["type"] == "calc_fma_mass":
                m, a = random.randint(2, 10), random.randint(2, 6)
                f = m * a
                text = item["context"].format(f=f, a=a)
                ans = f"{m} kg"
            elif item["type"] == "calc_fma_accel":
                m, a = random.randint(2, 10), random.randint(2, 8)
                f = m * a
                text = item["context"].format(f=f, m=m)
                ans = f"{a} m/s²"
            elif item["type"] == "calc_weight":
                m = random.randint(5, 50)
                text = item["context"].format(m=m)
                ans = f"{m * 10} N"
            elif item["type"] == "calc_net_accel":
                f1 = random.randint(300, 800)
                text = item["context"].format(f1=f1)
                ans = "Net force is 0 N. It will not accelerate."
                
            rule = f"The student must show working and reach the final answer of: {ans}. Do not penalize if they omit intermediate working as long as the final calculation is correct."
            item.update({"text": text, "options": [], "grading_rule": rule, "ans": ans})
            return item

def get_next_question():
    mode = st.session_state.get('selection_mode', 'Random')
    quiz_style = st.session_state.get('quiz_style', 'Both')
    
    if mode == "Random":
        return generate_forces_problem(quiz_style=quiz_style)
        
    # Build a fresh queue if empty
    if 'question_queue' not in st.session_state or not st.session_state.question_queue:
        if mode == "Quiz":
            st.session_state.quiz_score = 0
            st.session_state.quiz_completed = False
            
        mcq_pool, written_pool = get_all_problems()
        combined_pool = []
        if quiz_style in ["Multiple Choice", "Both"]: combined_pool.extend(mcq_pool)
        if quiz_style in ["Written Answers", "Both"]: combined_pool.extend(written_pool)
        
        random.shuffle(combined_pool)
        
        # Limit Quiz mode to 10 questions for brevity
        if mode == "Quiz" and len(combined_pool) > 10:
            combined_pool = combined_pool[:10]
            
        st.session_state.question_queue = combined_pool
        
    if mode == "Quiz" and not st.session_state.question_queue:
        st.session_state.quiz_completed = True
        return None
        
    raw_item = st.session_state.question_queue.pop(0)
    
    # Process the raw item from the queue into the generated format
    if raw_item.get("mode") == "MCQ":
        options = raw_item["distractors"] + [raw_item["ans"]]
        random.shuffle(options)
        raw_item["options"] = options
        raw_item["text"] = raw_item.get("q", raw_item.get("text"))
        return raw_item
    else:
        # Ensure the mode tag is safely passed to prevent KeyError
        raw_item["mode"] = "Written"
        
        if raw_item["class"] == 4:
            # We must regenerate variables if class 4 so it's not a template string
            if raw_item["type"] == "calc_net":
                f1, f2 = random.randint(500, 900), random.randint(100, 300)
                text = raw_item["context"].format(f1=f1, f2=f2) + "\n\nCalculate the net force and state its direction."
                ans = f"{f1 - f2} N forward"
            elif raw_item["type"] == "calc_fma":
                m, a = random.randint(2, 12), random.randint(2, 8)
                text = raw_item["context"].format(m=m, a=a)
                ans = f"{m * a} N"
            elif raw_item["type"] == "calc_fma_mass":
                m, a = random.randint(2, 10), random.randint(2, 6)
                f = m * a
                text = raw_item["context"].format(f=f, a=a)
                ans = f"{m} kg"
            elif raw_item["type"] == "calc_fma_accel":
                m, a = random.randint(2, 10), random.randint(2, 8)
                f = m * a
                text = raw_item["context"].format(f=f, m=m)
                ans = f"{a} m/s²"
            elif raw_item["type"] == "calc_weight":
                m = random.randint(5, 50)
                text = raw_item["context"].format(m=m)
                ans = f"{m * 10} N"
            elif raw_item["type"] == "calc_net_accel":
                f1 = random.randint(300, 800)
                text = raw_item["context"].format(f1=f1)
                ans = "Net force is 0 N. It will not accelerate."
                
            rule = f"The student must show working and reach the final answer of: {ans}. Do not penalize if they omit intermediate working as long as the final calculation is correct."
            raw_item.update({"text": text, "options": [], "grading_rule": rule, "ans": ans})
            return raw_item
            
        else:
            if raw_item["type"] == "define":
                raw_item["text"] = f"Define the following term:\n\n{raw_item['term']}"
            else:
                raw_item["text"] = f"{raw_item['term']}"
            rule = f"The student must articulate the core concept. Exact wording is not required. Core concept: {raw_item['ans']}"
            raw_item["grading_rule"] = rule
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
    # Reset queues on setting change
    st.session_state.question_queue = []
    st.session_state.quiz_score = 0
    st.session_state.quiz_completed = False

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
    if 'selection_mode' not in st.session_state: st.session_state.selection_mode = "Random"

    st.title("Motion & Forces Quiz 🚀")

    # FIXED COLUMNS: Gives the mobile gear icon enough space to render
    col_actions, col_set = st.columns([4, 1])
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
            st.radio("Selection Mode", ["Random", "Cyclical", "Rehearse", "Quiz"], key="selection_mode", on_change=handle_settings_change)
            st.radio("Quiz Style", ["Multiple Choice", "Written Answers", "Both"], key="quiz_style", on_change=handle_settings_change)
            st.radio("Camera Mode", ["None", "App", "Native"], key="camera_mode", horizontal=True, on_change=handle_settings_change)
            st.toggle("Canvas Controls", key="show_controls", on_change=handle_settings_change)

    if st.session_state.get('quiz_completed', False):
        st.success(f"🎉 Quiz Complete! You scored {st.session_state.quiz_score} points.")
        if st.button("Restart Quiz"):
            handle_settings_change()
            st.rerun()
        return

    if st.session_state.generating:
        with st.spinner("Loading next question..."):
            p_data = get_next_question()
            if p_data is None: 
                st.rerun() 
                
            st.session_state.science_problem_data = p_data
            if p_data["mode"] == "Written":
                st.session_state.problem_image_context = draw_question_image(p_data["text"], width_px=420, height_px=420)
            st.session_state.generating = False
            st.rerun()

    else:
        p_data = st.session_state.science_problem_data
        
        if p_data["mode"] == "MCQ":
            st.write(f"### {p_data['text']}")
            
            # FIXED UI LOOP: Draw all buttons first and record if one is clicked
            selected_opt = None
            for idx, opt in enumerate(p_data["options"]):
                if st.button(opt, use_container_width=True, key=f"mcq_{idx}_{st.session_state.problem_suite_refresh_id}"):
                    selected_opt = opt
                    
            # Render the feedback explicitly BELOW all the buttons so the UI doesn't jump
            if selected_opt is not None:
                is_correct = (selected_opt == p_data["ans"])
                if is_correct:
                    st.success("✅ Correct!")
                    if st.session_state.selection_mode == "Quiz": 
                        st.session_state.quiz_score += 1
                else:
                    st.error(f"❌ Incorrect. The correct answer is: {p_data['ans']}")
                    if st.session_state.selection_mode == "Rehearse":
                        st.session_state.question_queue.append(p_data) # Send to back of queue
        else:
            bg_image = st.session_state.problem_image_context
            problem_context = f"Question: {p_data['text']}\nGrading Rule: {p_data.get('grading_rule', '')}"
            
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
            if st.session_state.selection_mode == "Cyclical":
                st.session_state.question_queue.append(p_data) # Send to back of queue to loop
            st.session_state.generating = True
            st.session_state.problem_suite_refresh_id += 1 
            st.rerun()