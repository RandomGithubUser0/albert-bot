from dotenv import load_dotenv
from enums import ProblemType, SolverType

import os

load_dotenv()

# URLS

URLS = [
    "https://www.albert.io/adaptive/skill/b8e0fead-7e71-4b27-b633-ed11e82db4f1"
]

# Solver Config

SOLVER_TYPE = SolverType.LOCAL

SOLVER_MODELS = {
    SolverType.LOCAL:  "gemma-4-e4b", # "qwen2.5-vl-7b",
    SolverType.CLAUDE: "claude-haiku-4-5",
    SolverType.OPENAI: "gpt-4o",
    SolverType.GEMINI: "gemini-2.0-flash",
}

# Prompts

SYSTEM_PROMPT_STUD = """You are a math problem solver. You will be given a math question and must answer it correctly.
Always wrap your final answer in square brackets []. Example: [2] 
Try to keep additional sentences minimal, but if it helps you, feel free to show steps. 
"""

SYSTEM_PROMPTS = {
    ProblemType.MCQ: """This is a multiple choice question with one correct answer.
Answer choices are labeled [0]:, [1]:, [2]:, etc.
Reply with ONLY the index number of the correct choice.
Example: [1]""",

    ProblemType.CHOOSE_ALL: """This is a multiple choice question where one or more answers may be correct.
Answer choices are labeled [0]:, [1]:, [2]:, etc.
Reply with ONLY the index numbers of all correct choices as a list.
Example: [0, 2]""",

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

ALBERT_EMAIL = os.getenv("ALBERT_EMAIL")
ALBERT_PASSWORD = os.getenv("ALBERT_PASSWORD")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LOCAL_LLM_URL = os.getenv("LOCAL_LLM_URL", "http://localhost:1234/v1")

def system_prompt(problem_type: ProblemType) -> str:
    return SYSTEM_PROMPT_STUD + " " + SYSTEM_PROMPTS[problem_type]

# Logs

LOG_DIR = "logs"
SCREENSHOT_DIR = os.path.join(LOG_DIR, "screenshots")