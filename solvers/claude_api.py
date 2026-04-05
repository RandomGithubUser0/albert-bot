from .base import BaseSolver

class ClaudeSolver(BaseSolver):
    
    def __init__(self):
        """Initialize the Anthropic client and model config."""
        pass
    
    def feed(self, content: list) -> str:
        """Send prompt to Claude API and return response."""
        pass