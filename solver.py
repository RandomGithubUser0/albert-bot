import base64
import os
import config

from problemtype import ProblemType
from anthropic import Anthropic

client = Anthropic(
    api_key=config.ANTHROPIC_API_KEY,
)

def solveWithScreenshot(screenshot_bytes: bytes, current_type : ProblemType):
    image_data = base64.standard_b64encode(screenshot_bytes).decode("utf-8")
    message = client.messages.create(
        max_tokens=config.MAX_TOKENS,
        system = config.SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [{
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text", 
                    "text": config.PROMPTS[current_type]
                }
                ],
            }
        ],
        model=config.MODEL,
    )
    return message.content