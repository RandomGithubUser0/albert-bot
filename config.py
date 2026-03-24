from dotenv import load_dotenv
import os

load_dotenv()

# Anthropic
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-haiku-4-5-20251001"
MAX_TOKENS = 10

# Auth
ALBERT_EMAIL = os.getenv("ALBERT_EMAIL")
ALBERT_PASSWORD = os.getenv("ALBERT_PASSWORD")

# Paths
SCREENSHOTS_DIR = "screenshots"

# Bot behavior
CLICK_DELAY_MS = 500
SCREENSHOT_DELAY_MS = 1000