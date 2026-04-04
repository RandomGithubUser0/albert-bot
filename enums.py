from enum import Enum, auto

class SolverType(Enum):
    LOCAL = "local"
    API = "api"

class ProblemType(Enum):
    MCQ = "MCQ"
    CHOOSE_ALL = "CHOOSE_ALL"
    FITB = "FITB"
    INPUT = "INPUT"