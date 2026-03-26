from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from problemtype import ProblemType

import json
import re
import string
import time
import solver

import os

import config

URLS = [
    "https://www.albert.io/adaptive/practice/019d27e8-0ef9-78e4-b518-3420d3be6e3d"
]

NUMBER_TO_ALPHABET = both_cases_list = list(string.ascii_letters)
ALPHABET_TO_NUMBER = {}

for number, letter in enumerate(NUMBER_TO_ALPHABET):
    ALPHABET_TO_NUMBER[letter] = number

def sign_in(page: Page):
    page.goto("https://www.albert.io/log-in")

    time.sleep(1)

    page.fill('[data-testid="log-in--identifier"]', config.ALBERT_EMAIL)    
    page.fill('[data-testid="log-in--password"]', config.ALBERT_PASSWORD)
    
    time.sleep(1)

    page.click('[type="submit"]')

def skip_tour(page : Page):
    skip = page.query_selector('button:has-text("Skip Tour")')
    if skip:
        skip.click()

def get_question_type(page : Page):
    if page.query_selector('legend:has-text("Select one answer")'):
        return ProblemType.MCQ
    elif page.query_selector('legend:has-text("Select all that apply")'):
        return ProblemType.CHOOSEALL
    elif page.query_selector('legend:has-text("Select options below")'):
        return ProblemType.FITB

def has_diagram(page : Page):
    return page.query_selector('.image-supplement__image') is not None

def extract_question_text(page : Page):
    question = page.query_selector('.markdown-renderer-v2:not(.adaptive-practice-view__toolbar__title--redesigned) > .paragraph')
    math_elements = page.query_selector_all('script[type="math/tex"], script[type="math/tex; mode=display"]')

    combination = ''
    for text in math_elements:
        combination = combination + text.inner_text()

    print(question.inner_text() + combination)

def extract_answer_choices(page : Page):
    options = page.query_selector_all('.mcq-option__content')
    answer_choices = ""
    for i, option in enumerate(options):
        inner_text = re.sub(r'\s+', ' ', option.inner_text()).strip()
        answer_choices = answer_choices + " " + f"Option {NUMBER_TO_ALPHABET[i]}: {inner_text}"
    return answer_choices

def select_and_submit_answers(page : Page, answer_list):
    for letter in answer_list:
        time.sleep(0.5)
        to_number = ALPHABET_TO_NUMBER[letter]
        choice = page.query_selector(f'[data-testid="mcq-option-{to_number}"]')
        choice.click()
    submit = page.query_selector(':text("Submit Answer")')
    time.sleep(0.5)
    submit.click()

def move_on(page: Page):
    letsgo_button = page.query_selector(':text("Let\'s go")')
    next_button = page.query_selector(':text("Next Question")')
    if letsgo_button:
        letsgo_button.click()
    elif next_button:
        next_button.click()

def albert_is_completed(page: Page):
    achieved_advanced = page.query_selector(':text("You achieved \\"Advanced\\" on this skill level!")')
    reached_advanced = page.query_selector(':text("You achieved \\"Advanced\\" on this skill level!")')
    return (achieved_advanced is not None) or (reached_advanced is not None) 

os.makedirs(config.SCREENSHOTS_DIR, exist_ok=True)

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()

    sign_in(page)

    time.sleep(2)

    for URL in URLS:
        page.goto(URL)
        time.sleep(0.5)
        skip_tour(page)
        time.sleep(0.5)

        while not albert_is_completed(page):
            screenshot = page.screenshot(path=f"{config.SCREENSHOTS_DIR}/question.png")
            current_type = get_question_type(page)
            # while True:
            #   print(extract_answer_choices(page))
            #   time.sleep(5)
            answer = solver.solveWithScreenshot(screenshot, current_type)
            print(answer)
            response = answer[0].text.strip()

            print("response: " + response)        

            answers = json.loads(response) 

            select_and_submit_answers(page, answers)

            time.sleep(0.5)

            move_on(page)

            time.sleep(1)

        time.sleep(2)