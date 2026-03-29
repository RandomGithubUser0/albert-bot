from abc import ABC, abstractmethod

class BaseSolver(ABC):
    
    @abstractmethod
    def solve(self, prompt: str) -> str:
        """Send a prompt and return the model's response."""
        pass