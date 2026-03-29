from .base import BaseSolver

class LocalLLMSolver(BaseSolver):
    
    def __init__(self, model_path: str):
        """Load the local model from the given path."""
        pass
    
    def solve(self, prompt: str) -> str:
        """Run inference locally and return response."""
        pass