from openai import OpenAI
from enums import ProblemType
import config

client = OpenAI()

def feed(model: str, problem_type: ProblemType, content: list) -> str:
    system = config.system_prompt(problem_type)
    response = client.chat.completions.create(
        model=model,
        temperature=0,
        max_tokens=16384,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": content},
        ],
    )
    return response.choices[0].message.content
