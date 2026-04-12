from enums import ProblemType
from openai import OpenAI

import config

client = OpenAI(
    base_url = config.LOCAL_LLM_URL,
    api_key = "not-needed",
)

def feed(model : str, problem_type : ProblemType, content : list):
    response = client.chat.completions.create(
        model = model,  # must match exactly what LM Studio shows
        temperature = 0,
        max_tokens = 16384,
        messages = [
            {
                "role": "system",
                "content": config.system_prompt(problem_type)
            },
            {
                "role": "user",
                "content": content
            }
        ]
    )

    msg = response.choices[0].message
    return msg.content or getattr(msg, "reasoning_content", None) or ""