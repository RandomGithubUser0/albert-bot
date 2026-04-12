# utils.py
import base64
import httpx
import re
import ast

from playwright.sync_api import Browser

_http = httpx.Client(timeout=10)

def fetch_image_b64(url: str, browser: Browser) -> str:
    if url.endswith(".svg"):
        return _render_svg_b64(url, browser)

    data = _http.get(url).content
    return base64.b64encode(data).decode()


def _render_svg_b64(url: str, browser: Browser) -> str:
    """
    Open the SVG in a headless browser page, screenshot it, and return
    the result as base64. 
    """
    page = browser.new_page()
    page.goto(url)
    png_data = page.screenshot()
    page.close()
    return base64.b64encode(png_data).decode()

def clean_inner_text(text: str) -> str:
    """Remove MathJax duplicate text artifacts."""
    text = text.replace('\n', ' ')
    
    words = text.split()
    cleaned_words = []
    for word in words:
        if not cleaned_words or word != cleaned_words[-1]:
            cleaned_words.append(word)
    cleaned_text = " ".join(cleaned_words)
    
    cleaned_text = re.sub(r'(\([^)]+\))\s+\1', r'\1', cleaned_text)
    cleaned_text = re.sub(r'(\d+)\s+\1', r'\1', cleaned_text)
    
    return cleaned_text

def parse_llm_answer(response: str) -> list:
    """
    Extract the answer from the model's response and convert it to a list.
    Takes the LAST bracketed expression in case the model adds explanation before the answer.
    """
    matches = re.findall(r'\[.*?\]', response)
    if not matches:
        raise ValueError(f"No answer found in response: {response}")
    return ast.literal_eval(matches[-1])