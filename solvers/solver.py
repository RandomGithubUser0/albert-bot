from enums import ProblemType, SolverType
from solvers import local_llm, claude_api, openai_api, gemini_api
import config

_SOLVERS = {
    SolverType.LOCAL:  local_llm,
    SolverType.CLAUDE: claude_api,
    SolverType.OPENAI: openai_api,
    SolverType.GEMINI: gemini_api,
}

def feed(problem_type: ProblemType, content: list) -> str:
    solver = _SOLVERS[config.SOLVER_TYPE]
    model = config.SOLVER_MODELS[config.SOLVER_TYPE]
    return solver.feed(model, problem_type, content)
