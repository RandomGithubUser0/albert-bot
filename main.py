from playwright.sync_api import sync_playwright
from scraper import html_scraper
from solvers import solver
from enums import CompletionStatus

import os
import time
import config
import utils
import logger

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

    logger.new_session(config.LOG_DIR)

    for url in config.URLS:
        scraper.setup_page(url)
        status = scraper.albert_is_completed()
        print(status)
        while status == CompletionStatus.NOT_COMPLETED:
            time.sleep(2)
            problem_type = scraper.get_type()
            if problem_type is None:
                print("Warning: could not detect problem type, retrying...")
                continue
            content = scraper.parse_question(problem_type)
            print(f"\n--- PROMPT ({problem_type}) ---")
            for block in content:
                if block["type"] == "image_url":
                    print({"type": "image_url", "url": block["image_url"]["url"][:40] + "..."})
                else:
                    print(block)
            print("--- END PROMPT ---\n")
            raw = solver.feed(problem_type, content)
            print(raw)
            result = utils.parse_llm_answer(raw)
            print(result)
            scraper.input_answers(result, problem_type)
            time.sleep(1)
            correct = scraper.get_answer_result()
            logger.log_question(url, problem_type, content, result, correct)
            scraper.move_on()
            status = scraper.albert_is_completed()
        if status == CompletionStatus.JUST_COMPLETED:
            logger.log_complete_albert(url)
