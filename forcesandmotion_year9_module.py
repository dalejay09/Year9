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
        {"class": 1, "mode": "MCQ", "q": "The pulling force transmitted through a