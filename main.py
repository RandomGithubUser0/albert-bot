from playwright.sync_api import sync_playwright
from scraper import html_scraper

import os
import time
import config

os.makedirs(config.LOG_DIR, exist_ok=True)
os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    scraper = html_scraper.Scraper(page, browser)
    scraper.login()

    time.sleep(0.5)

    # main loop

    # TODO finish pipeline
    # TODO handle FITB
    # TODO UI maybe??

    for url in config.URLS:
        scraper.setup_page(url)
        print(scraper.albert_is_completed())
        while not scraper.albert_is_completed():
            time.sleep(2)
            result = scraper.parse_question()
            for item in result:
                if item["type"] == "text":
                    print(item)
                else:
                    print({"type": "image", "data": item["data"][:30] + "..."})  # truncate b64
            
