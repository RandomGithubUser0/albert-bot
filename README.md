# Albert Bot

Automates Albert.io adaptive skill assignments using a local or cloud LLM and Playwright.

## Disclaimer (Read This First)

This project is intended **strictly for educational and experimental purposes only**.

* It was created as a **personal side project** to explore automation, Playwright, and working with **local and cloud-based large language models (LLMs)**.
* It is **not intended to be used to gain an unfair advantage**, bypass academic policies, or violate the terms of service of any platform.
* Users are solely responsible for how they use this software. Misuse may violate school rules or platform policies.

If you are a student, you should only use this project in ways that align with your institution’s academic integrity guidelines.

## Requirements

* Python 3.10+
* [LM Studio](https://lmstudio.ai) (for `LOCAL` solver) or API keys for Claude / OpenAI / Gemini

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

* `URLS` — list of Albert.io skill/practice URLs to complete
* `SOLVER_TYPE` — `SolverType.LOCAL`, `SolverType.CLAUDE`, `SolverType.OPENAI`, or `SolverType.GEMINI`
* `SOLVER_MODELS` — model name for each solver

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

* `session.jsonl` — per-question log entries
* `stats.json` — session summary (correct/incorrect, level ups/downs, etc.)
