from dotenv import load_dotenv
from enums import ProblemType, SolverType

import os

load_dotenv()

LOG_DIR = "logs"
SESSION_LOG = os.path.join(LOG_DIR, "session.log")
ERROR_LOG = os.path.join(LOG_DIR, "errors.log")
SCREENSHOT_DIR = os.path.join(LOG_DIR, "screenshots")

URLS = [
    "https://www.albert.io/adaptive/practice/019d1100-a3c6-7102-aab5-a9da52563e6d"
]

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

ALBERT_EMAIL = os.getenv("ALBERT_EMAIL")
ALBERT_PASSWORD = os.getenv("ALBERT_PASSWORD")