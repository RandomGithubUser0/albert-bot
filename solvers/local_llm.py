from .base import BaseSolver
from enums import ProblemType

import ollama
import config

class LocalLLMSolver(BaseSolver):
    model : str 

    def __init__(self, model: str):
        """Load the local model from the given path."""
        self.model = model
    
    def feed(self, content: list) -> str:
        response = ollama.chat(
            model = self.model,
            messages = [
                {
                    "role": "system",
                    "content": config.SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        return response["message"]["content"]
    
    def solve(self, content: list) -> str:
        response = self.feed(content)
        return ""