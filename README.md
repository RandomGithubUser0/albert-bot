# Albert Bot

Automates Albert.io adaptive skill assignments using a local or cloud LLM and Playwright.

## Requirements

- Python 3.10+
- [LM Studio](https://lmstudio.ai) (for `LOCAL` solver) or API keys for Claude / OpenAI / Gemini

## Setup

```bash
pip install -r requirements.txt
playwright install chromium
```

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `config.py` to set:
- `URLS` — list of Albert.io skill/practice URLs to complete
- `SOLVER_TYPE` — `SolverType.LOCAL`, `SolverType.CLAUDE`, `SolverType.OPENAI`, or `SolverType.GEMINI`
- `SOLVER_MODELS` — model name for each solver

## Running

**Local solver (LM Studio):**

Start LM Studio's local server with:

```bash
lms server start
```

(Port should be 1234)

then:

```bash
python main.py
```

**Cloud solver:**

Set the appropriate API key in `.env`, set `SOLVER_TYPE` in `config.py`, then:

```bash
python main.py
```

## Logs

Each run creates a timestamped folder under `logs/` containing:
- `session.jsonl` — per-question log entries
- `stats.json` — session summary (correct/incorrect, level ups/downs, etc.)