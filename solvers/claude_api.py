import anthropic
import config
from enums import ProblemType

client = anthropic.Anthropic()

def _convert_content(content: list) -> list:
    """Convert OpenAI-format content blocks to Anthropic format."""
    result = []
    for block in content:
        if block["type"] == "text":
            result.append({"type": "text", "text": block["text"]})
        elif block["type"] == "image_url":
            url = block["image_url"]["url"]
            # url is "data:image/png;base64,<data>"
            data = url.split(",", 1)[1]
            result.append({
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": data,
                },
            })
    return result

def feed(model: str, problem_type: ProblemType, content: list) -> str:
    system = config.SYSTEM_PROMPT_STUD + " " + config.SYSTEM_PROMPTS[problem_type]
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system,
        messages=[
            {"role": "user", "content": _convert_content(content)}
        ],
    )
    return response.content[0].text
