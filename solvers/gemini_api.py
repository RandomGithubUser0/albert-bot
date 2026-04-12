import base64
import google.generativeai as genai
from enums import ProblemType
import config

genai.configure(api_key=config.GEMINI_API_KEY)

_model_cache: dict = {}

def _get_model(model: str, problem_type: ProblemType):
    key = (model, problem_type)
    if key not in _model_cache:
        _model_cache[key] = genai.GenerativeModel(
            model_name=model,
            system_instruction=config.system_prompt(problem_type),
        )
    return _model_cache[key]

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
    gemini = _get_model(model, problem_type)
    response = gemini.generate_content(
        _convert_content(content),
        generation_config=genai.GenerationConfig(temperature=0, max_output_tokens=4096),
    )
    return response.text
