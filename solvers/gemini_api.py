import base64
import google.generativeai as genai
from enums import ProblemType
import config

genai.configure(api_key=config.GEMINI_API_KEY)

def _convert_content(content: list) -> list:
    parts = []
    for block in content:
        if block["type"] == "text":
            parts.append(block["text"])
        elif block["type"] == "image_url":
            data = block["image_url"]["url"].split(",", 1)[1]
            parts.append({"mime_type": "image/png", "data": base64.b64decode(data)})
    return parts

def feed(model: str, problem_type: ProblemType, content: list) -> str:
    system = config.SYSTEM_PROMPT_STUD + " " + config.SYSTEM_PROMPTS[problem_type]
    gemini = genai.GenerativeModel(model_name=model, system_instruction=system)
    response = gemini.generate_content(
        _convert_content(content),
        generation_config=genai.GenerationConfig(temperature=0, max_output_tokens=4096),
    )
    return response.text
