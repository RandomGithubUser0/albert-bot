from dotenv import load_dotenv
from enums import ProblemType, SolverType

import os

# URLS

URLS = [
    "https://www.albert.io/adaptive/practice/019d56a3-f5ba-7474-b117-deb46ac029c0"
]

# Solver Config

SOLVER_CONFIG = {
    "has_image": {
        "type": SolverType.API,
        "model": "claude-haiku-4-5",
        "max_tokens": 1024
    },
    "no_image": {
        "type": SolverType.LOCAL,
        "model": "",
        "max_tokens": 1024
    }
}

# Prompts

SYSTEM_PROMPT_STUD = "test"

SYSTEM_PROMPTS = {
    ProblemType.MCQ: "test"    
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