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

_PYTHON_LITERALS = {'True', 'False', 'None'}

def _quote_bare_words(expr: str) -> str:
    """Quote unquoted alphabetic tokens so ast.literal_eval can handle them, e.g. [complex] → ["complex"]."""
    return re.sub(
        r'(?<!["\'\w])([A-Za-z][A-Za-z0-9_]*)(?!["\'\w])',
        lambda m: m.group() if m.group() in _PYTHON_LITERALS else f'"{m.group()}"',
        expr
    )

def _all_bracket_exprs(s: str) -> list:
    """Return all top-level balanced [...] expressions in s, in order."""
    results = []
    i = 0
    while i < len(s):
        if s[i] == '[':
            depth = 0
            start = i
            while i < len(s):
                if s[i] == '[':
                    depth += 1
                elif s[i] == ']':
                    depth -= 1
                    if depth == 0:
                        results.append(s[start:i + 1])
                        i += 1
                        break
                i += 1
        else:
            i += 1
    return results

def parse_llm_answer(response: str) -> list:
    """
    Extract the answer from the model's response and convert it to a list.

    Handles three output patterns:
      [2.5, -1]          → [2.5, -1]       flat list (ideal)
      [[-3], [-2], [0]]  → [-3, -2, 0]     nested single-value lists
      [2.5]\\n[-1]        → [2.5, -1]       one bracket per line
    """
    exprs = _all_bracket_exprs(response)
    if not exprs:
        raise ValueError(f"No answer found in response: {response}")

    parsed = [ast.literal_eval(_quote_bare_words(e)) for e in exprs]

    # Multiple single-value lists → model answered one per line or nested
    if len(parsed) > 1 and all(isinstance(x, list) and len(x) == 1 for x in parsed):
        return [x[0] for x in parsed]

    # Single expression (normal case)
    result = parsed[-1]
    if not isinstance(result, list):
        result = [result]
    # Flatten [[a], [b], [c]] → [a, b, c]
    if result and all(isinstance(x, list) and len(x) == 1 for x in result):
        result = [x[0] for x in result]
    return result