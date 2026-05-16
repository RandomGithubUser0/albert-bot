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
    """Return all top-level balanced [...] expressions as (expr, start, end) tuples."""
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
                        results.append((s[start:i + 1], start, i + 1))
                        i += 1
                        break
                i += 1
        else:
            i += 1
    return results

def parse_llm_answer(response: str) -> list:
    """
    Extract the answer from the model's response and convert it to a list.

    Handles these output patterns:
      [2.5, -1]          → [2.5, -1]   flat list (ideal)
      [[-3], [-2], [0]]  → [-3, -2, 0] nested single-value lists
      [2.5]\\n[-1]        → [2.5, -1]   consecutive single-value brackets

    Label patterns like [0]: are filtered. When there are multiple groups of
    consecutive single-value brackets separated by blank lines, only the last
    group is used.
    """
    raw = _all_bracket_exprs(response)
    if not raw:
        raise ValueError(f"No answer found in response: {response}")

    # Filter out label patterns: [n]: (index labels echoed from the question)
    filtered = [(expr, start, end) for expr, start, end in raw
                if end >= len(response) or response[end] != ':']
    if not filtered:
        filtered = raw  # nothing survived the filter, fall back

    parsed = [(ast.literal_eval(_quote_bare_words(expr)), start, end)
              for expr, start, end in filtered]

    # Group consecutive single-value brackets — blank line breaks the group
    def is_single(val):
        return isinstance(val, list) and len(val) == 1

    if len(parsed) > 1 and all(is_single(v) for v, _, _ in parsed):
        groups = []
        group = [parsed[0]]
        for i in range(1, len(parsed)):
            _, prev_end = group[-1][1], group[-1][2]
            _, cur_start, _ = parsed[i]
            between = response[prev_end:cur_start]
            if re.search(r'\n\s*\n', between):
                groups.append(group)
                group = [parsed[i]]
            else:
                group.append(parsed[i])
        groups.append(group)
        last_group = groups[-1]
        return [v[0] for v, _, _ in last_group]

    # Single expression or multi-value list (normal case)
    result = parsed[-1][0]
    if not isinstance(result, list):
        result = [result]
    # Flatten [[a], [b], [c]] → [a, b, c]
    if result and all(isinstance(x, list) and len(x) == 1 for x in result):
        result = [x[0] for x in result]
    return result