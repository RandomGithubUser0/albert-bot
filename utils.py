# utils.py
import base64
import httpx
from playwright.sync_api import Browser

def fetch_image_b64(url: str, browser: Browser) -> str:
    """
    Fetch an image from a URL and return it as a base64-encoded string.
    """
    if url.endswith(".svg"):
        return _render_svg_b64(url, browser)
    
    data = httpx.get(url).content
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
    lines = [l for l in text.split("\n") if l.strip()]  # remove empty lines
    half = len(lines) // 2
    if lines[:half] == lines[half:]:
        return " ".join(lines[:half])
    return " ".join(lines)