from dotenv import load_dotenv
from enums import ProblemType, SolverType

import os

# URLS

URLS = [
    "https://www.albert.io/adaptive/practice/019b93ac-d2ba-799b-bf67-9126fa9abd55"
]

# Solver Config

SOLVER_TYPE = SolverType.LOCAL
SOLVER_MODEL = "qwen2.5-vl-7b"

# Prompts

SYSTEM_PROMPT_STUD = """You are a math problem solver. You will be given a math question and must answer it correctly.
Always wrap your final answer in square brackets []. Example: [2] 
Try to keep additional sentences minimal, but if it helps you, feel free to show steps. 
"""

SYSTEM_PROMPTS = {
    ProblemType.MCQ: """This is a multiple choice question with one correct answer.
Reply with the index of the correct answer choice.
Example: [0]""",

    ProblemType.FITB: """This is a fill in the blank question.
Step 1: Solve the math and find the value for each blank.
Step 2: For each blank, find which CHOICE number matches that value. The index is the number after "CHOICE", starting from 0.
Step 3: Reply with those indices in order as a list.
Example: if BLANK0=CHOICE2 and BLANK1=CHOICE0, reply [2, 0].""",

    ProblemType.INPUT: """This is a free response question. Answer precisely as instructed in the question.
Wrap your answer in brackets.
Example: [(30, 1)] or [42] or [x = 5]"""
}

# .env

load_dotenv()

ALBERT_EMAIL = os.getenv("ALBERT_EMAIL")
ALBERT_PASSWORD = os.getenv("ALBERT_PASSWORD")

# Logs

LOG_DIR = "logs"
SESSION_LOG = os.path.join(LOG_DIR, "session.log")
ERROR_LOG = os.path.join(LOG_DIR, "errors.log")
SCREENSHOT_DIR = os.path.join(LOG_DIR, "screenshots")