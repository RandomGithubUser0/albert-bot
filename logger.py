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
    Append one JSONL entry to session.jsonl describing a question attempt.

    Image blocks (type == "image_url") in content are replaced with
    {"type": "image_url", "skipped": True} to keep the log file small.

    Entry fields: timestamp, url, problem_type, content, llm_answer, correct, error.
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

    with open(os.path.join(_session_dir, "session.jsonl"), "a") as f:
        f.write(json.dumps(entry) + "\n")


def log_error(url: str, error: str):
    """
    Append one JSONL error entry to session.jsonl.

    Entry fields: timestamp, url, event="error", error.
    Does nothing if new_session() has not been called.
    """
    if _session_dir is None:
        return

    entry = {
        "timestamp": datetime.now().isoformat(),
        "url": url,
        "event": "error",
        "error": error,
    }

    with open(os.path.join(_session_dir, "session.jsonl"), "a") as f:
        f.write(json.dumps(entry) + "\n")


def update_stats(
    problem_type: ProblemType,
    correct: bool = None,
    fell_back: bool = False,
    albert_completed: bool = False,
):
    """
    Update the in-memory _stats dict for one question outcome, then rewrite stats.json.

    Stats structure:
    {
        "start_time": str,
        "end_time": str | None,
        "urls_attempted": int,
        "alberts_completed": int,
        "fell_back": int,
        "questions": {
            "total": int,
            "correct": int,
            "incorrect": int,
            "errors": int,
            "by_type": {
                "<ProblemType.value>": {
                    "total": int,
                    "correct": int,
                    "incorrect": int,
                    "errors": int,
                }
            }
        }
    }

    Does nothing if new_session() has not been called.
    """
    if _stats is None:
        return

    if albert_completed:
        _stats["alberts_completed"] += 1

    if fell_back:
        _stats["fell_back"] += 1

    q = _stats["questions"]
    q["total"] += 1

    if correct is True:
        q["correct"] += 1
    elif correct is False:
        q["incorrect"] += 1
    elif correct is None:
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
    elif correct is None:
        bt["errors"] += 1

    with open(os.path.join(_session_dir, "stats.json"), "w") as f:
        json.dump(_stats, f, indent=2)


def close_session():
    """
    Write the final end_time to stats.json.

    Does nothing if new_session() has not been called.
    """
    if _stats is None:
        return

    _stats["end_time"] = datetime.now().isoformat()

    with open(os.path.join(_session_dir, "stats.json"), "w") as f:
        json.dump(_stats, f, indent=2)