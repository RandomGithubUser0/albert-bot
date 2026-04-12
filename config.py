from dotenv import load_dotenv
from enums import ProblemType, SolverType

import os

load_dotenv()

# URLS

TEXT = """

https://www.albert.io/adaptive/skill/39d8b103-74ca-48c5-b15e-fcff36f1fd9f 

https://www.albert.io/adaptive/skill/2b47b53f-db2d-472a-bd77-acaf816d5879 
https://www.albert.io/adaptive/skill/2d8f3dd7-e4f6-495a-8697-9bb81c33558a 

https://www.albert.io/adaptive/skill/60b19c73-9d84-4ab5-8eed-36e937c7b21a 

https://www.albert.io/adaptive/skill/59e1ddc6-b035-4f05-aafb-b8c1540d25e6 
https://www.albert.io/adaptive/skill/d0ac0017-c84d-4440-acfa-657a3f348ab2 
https://www.albert.io/adaptive/skill/05a0f464-54ba-4668-9a85-e3a64a80abc2 

https://www.albert.io/adaptive/skill/e861f279-8f31-4539-88e5-224c21400911 
https://www.albert.io/adaptive/skill/a0a6814a-cee7-4fc3-9ddf-f527dd680359 
https://www.albert.io/adaptive/skill/9782b26a-1cd4-413b-b0aa-74d9d5e1f736 
https://www.albert.io/adaptive/skill/e8b5240e-ce12-490f-9f08-7ba5b8e94669 

https://www.albert.io/adaptive/skill/1f882f88-a92e-41b5-ba7e-fc3a59625609 

https://www.albert.io/adaptive/skill/d29cf11c-2c17-4352-8655-fabdaeb70f25 
https://www.albert.io/adaptive/skill/615ad66f-0254-4909-a75a-a64b94b42eb2 

https://www.albert.io/adaptive/skill/95602d73-3917-456d-8617-640c93148bfe 
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