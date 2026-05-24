from dotenv import load_dotenv
from enums import ProblemType, SolverType

import os

load_dotenv()

# URLS

TEXT = """
https://www.albert.io/adaptive/skill/95356190-e483-4f2b-8004-d213724b232c 
https://www.albert.io/adaptive/skill/8a34b30c-e5e0-4955-89e8-ed6802dda7e5 
https://www.albert.io/adaptive/skill/8b61d82e-3aca-4d19-af97-a2c8891b64a1 
https://www.albert.io/adaptive/skill/1ecbdae9-2cad-4de3-9641-4ba692011158 
https://www.albert.io/adaptive/skill/53add8d0-a379-42ca-98a9-d01c28f7836a 

https://www.albert.io/adaptive/skill/2a67d379-88e3-448a-bce9-4e9ff95fd01c
https://www.albert.io/adaptive/skill/75214c4b-ac58-43fb-a67f-e00fe93eb4b0
https://www.albert.io/adaptive/skill/f9aa0f56-d960-4d66-8a0b-3445dd6ba2a3 

"""
URLS = [line.strip() for line in TEXT.splitlines() if line.strip()]

# Solver Config

SOLVER_TYPE = SolverType.LOCAL

SOLVER_MODELS = {
    SolverType.LOCAL:  "gemma-4-e4b", # "qwen2.5-vl-7b",
    SolverType.CLAUDE: "claude-haiku-4-5",
    SolverType.OPENAI: "gpt-4o",
    SolverType.GEMINI: "gemini-2.5-flash",
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

    ProblemType.INPUT: """This is a free response question with one or more input boxes labeled INPUT 0, INPUT 1, etc.
Answer each input box in order. Wrap ALL answers together in ONE flat list.
Never nest lists. Always use this format:
Single input: [-3]
Multiple inputs: [-3, 0, 5]"""
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