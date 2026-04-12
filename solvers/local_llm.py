from enums import ProblemType
from openai import OpenAI

import config

client = OpenAI(
    base_url = "http://localhost:1234/v1",
    api_key = "lm studio 67 lmao", # doesn't matter
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

    return response.choices[0].message.content