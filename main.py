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

    scraper = html_scraper.Scraper(page)
    scraper.login()

    time.sleep(0.5)

    # main loop

    for url in config.URLS:
        print('e')
        scraper.setup_page(url)
        print('reached')
        print(scraper.albert_is_completed())
        while not scraper.albert_is_completed():
            time.sleep(0.5)
            problemType = scraper.get_type()
            if problemType:
                print(problemType.value)