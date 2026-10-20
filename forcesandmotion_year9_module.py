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
from pydantic import BaseModel

import ai_marking_component

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

    # 50/50 Likelihood Router
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
def draw_question_image