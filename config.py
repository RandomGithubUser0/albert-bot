from dotenv import load_dotenv
from enums import ProblemType, SolverType

import os

load_dotenv()

# URLS

TEXT = """
https://www.albert.io/adaptive/skill/e29f28dd-8c52-4d5f-8ad6-c886d873221d
https://www.albert.io/adaptive/skill/583cb0f3-18be-47b7-8eee-4809f2fb95d2 
https://www.albert.io/adaptive/skill/3658dbed-e200-4ae5-bed1-66b592720333 
https://www.albert.io/adaptive/skill/89fadddc-b242-458a-8714-0d36b2819828 
https://www.albert.io/adaptive/skill/3e154e3b-3dff-4b56-ace5-bdd63b3ef2fe 
https://www.albert.io/adaptive/skill/ce2b488b-3d9e-4982-a879-e7f60df1aa2c 
https://www.albert.io/adaptive/skill/ea638c9f-bdea-44fc-9d94-f0a744fb2474 
https://www.albert.io/adaptive/skill/b038eced-5ef7-4f94-85cb-044b078594e0 
https://www.albert.io/adaptive/skill/12d49fa7-7fd7-45ea-942f-bbc445aaca2b 
https://www.albert.io/adaptive/skill/b8924597-d26f-476a-8c2f-c5103c874e69
"""
URLS = [line.strip() for line in TEXT.splitlines() if line.strip()]

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