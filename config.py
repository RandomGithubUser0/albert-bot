from dotenv import load_dotenv
from enums import ProblemType, SolverType

import os

# URLS

URLS = [
    "https://www.albert.io/adaptive/practice/019d5144-5d17-7941-a29d-304ec5423489"
]

# Solver Config

SOLVER_TYPE = SolverType.LOCAL
SOLVER_MODEL = "gemma4:26b"

# Prompts

SYSTEM_PROMPT_STUD = """You are a math problem solver. You will be given a math question and must answer it correctly.
Always wrap your final answer in square brackets [].
Do not explain your reasoning. Only output the answer in brackets, nothing else."""

SYSTEM_PROMPTS = {
    ProblemType.MCQ: """This is a multiple choice question with one correct answer.
Reply with the index of the correct answer choice.
Example: [2]""",

    ProblemType.CHOOSE_ALL: """This is a multiple choice question where multiple answers may be correct.
Reply with the indices of all correct answer choices, comma separated.
Example: [0, 1, 3]""",

    ProblemType.FITB: "test",

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