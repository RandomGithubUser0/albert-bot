from enums import ProblemType

import httpx
import config

VLLM_URL = "http://localhost:8000/v1/chat/completions"

def feed(model: str, problem_type: ProblemType, content: list) -> str:
    response = httpx.post(VLLM_URL, json={
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "\n\n".join([
                    config.SYSTEM_PROMPT_STUD,
                    config.SYSTEM_PROMPTS[problem_type]
                ])
            },
            {
                "role": "user",
                "content": content
            }
        ]
    })
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
