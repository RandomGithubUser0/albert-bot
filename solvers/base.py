from abc import ABC, abstractmethod

class BaseSolver(ABC):
    
    @abstractmethod
    def feed(self, content: list) -> str:
        """Send a prompt and return the model's response."""
        pass