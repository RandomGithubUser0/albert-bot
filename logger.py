import json
import os
from datetime import datetime
from enums import ProblemType

_session_dir: str | None = None
_stats: dict | None = None


def new_session(base_log_dir: str) -> str:
    """
    Create a timestamped session folder inside base_log_dir.

    Folder name format: session_YYYY-MM-DD_HH-MM-SS/
    Creates two files inside:
      - stats.json   (initialized with start_time and zeroed counters)
      - session.jsonl (empty)

    Sets module-level _session_dir and _stats.
    Returns the session folder path.
    """
    global _session_dir, _stats

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    _session_dir = os.path.join(base_log_dir, f"session_{timestamp}")
    os.makedirs(_session_dir, exist_ok=True)

    _stats = {
        "start_time": datetime.now().isoformat(),
        "end_time": None,
        "urls_attempted": 0,
        "alberts_completed": 0,
        "level_downs": 0,
        "fell_back": 0,
        "questions": {
            "total": 0,
            "correct": 0,
            "incorrect": 0,
            "errors": 0,
            "by_type": {},
        },
    }

    with open(os.path.join(_session_dir, "stats.json"), "w") as f:
        json.dump(_stats, f, indent=2)

    open(os.path.join(_session_dir, "session.jsonl"), "w").close()

    return _session_dir


def log_question(
    url: str,
    problem_type: ProblemType,
    content: list,
    llm_answer: list,
    correct: bool = None,
    error: str = None,
):
    """
    Append one JSONL entry to session.jsonl and update question stats.

    Image blocks (type == "image_url") in content are replaced with
    {"type": "image_url", "skipped": True} to keep the log file small.

    correct=True increments correct, correct=False increments incorrect,
    correct=None increments errors.

    Does nothing if new_session() has not been called.
    """
    if _session_dir is None:
        return

    sanitized_content = [
        {"type": "image_url", "skipped": True} if b.get("type") == "image_url" else b
        for b in content
    ]

    entry = {
        "timestamp": datetime.now().isoformat(),
        "url": url,
        "problem_type": problem_type.value,
        "content": sanitized_content,
        "llm_answer": llm_answer,
        "correct": correct,
        "error": error,
    }

    _append_jsonl(entry)
    _update_question_stats(problem_type, correct)


def log_error(url: str, error: str):
    """
    Append one JSONL error entry to session.jsonl.

    Does not affect question counters. Use log_question with error= set
    when the error is tied to a specific question attempt.

    Does nothing if new_session() has not been called.
    """
    if _session_dir is None:
        return

    _append_jsonl({
        "timestamp": datetime.now().isoformat(),
        "url": url,
        "event": "error",
        "error": error,
    })


def log_level_down(url: str):
    """
    Log that Albert leveled the user down and increment level_downs.

    Does nothing if new_session() has not been called.
    """
    if _session_dir is None:
        return

    _append_jsonl({
        "timestamp": datetime.now().isoformat(),
        "url": url,
        "event": "level_down",
    })

    _stats["level_downs"] += 1
    _flush_stats()


def log_fallback(url: str):
    """
    Log a fallback event (e.g. LLM failed, used a default answer) and increment fell_back.

    Does nothing if new_session() has not been called.
    """
    if _session_dir is None:
        return

    _append_jsonl({
        "timestamp": datetime.now().isoformat(),
        "url": url,
        "event": "fallback",
    })

    _stats["fell_back"] += 1
    _flush_stats()


def log_complete_albert(url: str):
    """
    Log that an Albert skill was fully completed and increment alberts_completed.

    Does nothing if new_session() has not been called.
    """
    if _session_dir is None:
        return

    _append_jsonl({
        "timestamp": datetime.now().isoformat(),
        "url": url,
        "event": "albert_completed",
    })

    _stats["alberts_completed"] += 1
    _flush_stats()


def close_session():
    """
    Write the final end_time to stats.json.

    Does nothing if new_session() has not been called.
    """
    if _stats is None:
        return

    _stats["end_time"] = datetime.now().isoformat()
    _flush_stats()


# --- private helpers ---

def _append_jsonl(entry: dict):
    with open(os.path.join(_session_dir, "session.jsonl"), "a") as f:
        f.write(json.dumps(entry) + "\n")


def _flush_stats():
    with open(os.path.join(_session_dir, "stats.json"), "w") as f:
        json.dump(_stats, f, indent=2)


def _update_question_stats(problem_type: ProblemType, correct: bool | None):
    q = _stats["questions"]
    q["total"] += 1

    if correct is True:
        q["correct"] += 1
    elif correct is False:
        q["incorrect"] += 1
    else:
        q["errors"] += 1

    key = problem_type.value
    if key not in q["by_type"]:
        q["by_type"][key] = {"total": 0, "correct": 0, "incorrect": 0, "errors": 0}

    bt = q["by_type"][key]
    bt["total"] += 1
    if correct is True:
        bt["correct"] += 1
    elif correct is False:
        bt["incorrect"] += 1
    else:
        bt["errors"] += 1

    _flush_stats()
