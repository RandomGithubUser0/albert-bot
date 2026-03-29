from dotenv import load_dotenv
from enums import ProblemType, SolverType

import os

load_dotenv()

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