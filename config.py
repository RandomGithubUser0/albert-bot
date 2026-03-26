from dotenv import load_dotenv
import os

from problemtype import ProblemType

load_dotenv()

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 20

# Auth
ALBERT_EMAIL = os.getenv("ALBERT_EMAIL")
ALBERT_PASSWORD = os.getenv("ALBERT_PASSWORD")

# Paths
SCREENSHOTS_DIR = "screenshots"

# Bot behavior
CLICK_DELAY_MS = 500
SCREENSHOT_DELAY_MS = 1000

# Prompts
SYSTEM_PROMPT = """
    You are an answer extraction tool.
    You ONLY output a JSON array of answer letters (lowercase).
    Never explain. Never add text. Only output the array.
    """

GENERAL_PROMPT = """"
    This is a multiple choice question. 
    Respond with ONLY a JSON array of the correct answer letter(s).
    Examples: ["a"] or ["a", "b"]
    """
PROMPTS = {
    ProblemType.MCQ : "This is a multiple choice question with ONE correct answer. Reply with ONLY a JSON array with one letter. Example: [a]",
    ProblemType.CHOOSEALL : "This is a choose all question with potential multiple correct answers. Reply with ONLY a JSON array with the letter choices. Example: [a, b, c]",
    ProblemType.FITB : "This is a fill in the blank problem with multiple prompts. Here are the options: UNIMPLEMENTED, RETURN [a]"
}

LINKS = [
    
]