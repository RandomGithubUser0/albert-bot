from playwright.sync_api import sync_playwright
from scraper import html_scraper
from solvers import solver
from enums import CompletionStatus, ProblemType

import os
import time
import config
import utils
import logger


def _fallback_answer(problem_type: ProblemType, content: list) -> list:
    """Return a generic answer when the LLM fails to produce a valid one."""
    if problem_type == ProblemType.FITB:
        blank_count = sum(
            1 for b in content
            if b.get("type") == "text" and "|| BLANK" in b.get("text", "")
        )
        return [0] * max(blank_count, 1)
    return [0]


os.makedirs(config.LOG_DIR, exist_ok=True)
os.makedirs(config.SCREENSHOT_DIR, exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    scraper = html_scraper.Scraper(page, browser)
    scraper.login()
    time.sleep(0.5)

    logger.new_session(config.LOG_DIR)

    for url in config.URLS:
        logger.log_new_url(url)
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

            fell_back = False
            try:
                raw = solver.feed(problem_type, content)
                print(raw)
                result = utils.parse_llm_answer(raw)
            except Exception as e:
                print(f"LLM error: {e}")
                logger.log_error(url, str(e))
                result = _fallback_answer(problem_type, content)
                logger.log_fallback(url)
                fell_back = True

            print(result)

            try:
                scraper.input_answers(result, problem_type)
            except Exception as e:
                print(f"Input error: {e}")
                logger.log_error(url, str(e))

            time.sleep(1)
            correct = scraper.get_answer_result()
            logger.log_question(url, problem_type, content, result, correct,
                                error="fallback" if fell_back else None)

            scraper.move_on()
            status = scraper.albert_is_completed()

        if status == CompletionStatus.JUST_COMPLETED:
            logger.log_complete_albert(url)
        elif status == CompletionStatus.ALREADY_COMPLETED:
            logger.log_already_completed(url)

    logger.close_session()

    input("Done. Press Enter to close the browser...")
    browser.close()
