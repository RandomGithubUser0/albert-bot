from playwright.sync_api import sync_playwright
import time

import config

URLS = [
    "https://www.albert.io/adaptive/skill/95356190-e483-4f2b-8004-d213724b232c",
    "https://www.albert.io/adaptive/skill/8a34b30c-e5e0-4955-89e8-ed6802dda7e5",
    "https://www.albert.io/adaptive/skill/8b61d82e-3aca-4d19-af97-a2c8891b64a1",
]

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.albert.io/log-in")

    time.sleep(2)

    page.fill('[data-testid="log-in--identifier"]', config.ALBERT_EMAIL)    
    page.fill('[data-testid="log-in--password"]', config.ALBERT_PASSWORD)

    time.sleep(1)

    page.click('[type="submit"]')

    time.sleep(2)

    for URL in URLS:
        page.goto(URL)
        time.sleep(2)
        skip = page.query_selector('button:has-text("Skip Tour")')
        if skip:
            skip.click()

        time.sleep(0.5)

        is_fitb = page.query_selector('[data-testid="fitb-dropdown_select-option"]')
        if is_fitb:
            print("ok")
            # fill in the blank flow
        else:
            print("god damn")
            # MCQ flow


        screenshot = page.screenshot()


        
        time.sleep(1000)