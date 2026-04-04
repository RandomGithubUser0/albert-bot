from enum import Enum, auto

class SolverType(Enum):
    LOCAL = "local"
    API = "api"

class ProblemType(Enum):
    MCQ = auto()
    CHOOSE_ALL = auto()
    FITB = auto()
    INPUT = auto()