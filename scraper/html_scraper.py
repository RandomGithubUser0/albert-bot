from playwright.sync_api import Browser, Page, TimeoutError
from enums import ProblemType
from scraper import queries
from scraper.parser import Parser

import config
import time


class Scraper(Parser):
    page: Page
    browser: Browser

    def __init__(self, page: Page, browser: Browser):
        self.page = page
        self.browser = browser

    def login(self):
        self.page.goto("https://www.albert.io/log-in")
        self.page.fill(queries.LOGIN_IDENTIFIER, config.ALBERT_EMAIL)
        self.page.fill(queries.LOGIN_PASSWORD, config.ALBERT_PASSWORD)
        time.sleep(0.5)
        self.page.click(queries.LOGIN_BUTTON)

    def setup_page(self, url: str):
        self.page.goto(url)
        try:
            skip = self.page.wait_for_selector(queries.TOUR_BUTTON, timeout=1000)
            skip.click()
        except TimeoutError:
            print("Tour button didn't show up, skipping...")

    def get_type(self) -> ProblemType:
        for problem_type, query in queries.PROBLEM_TYPE_QUERIES.items():
            if self.page.query_selector(query) is not None:
                return problem_type
        return None

    def albert_is_completed(self) -> bool:
        return self.page.query_selector(queries.ADVANCED_COMPLETION_TEXT) is not None

    def input_answers(self, answer_list: list):
        problem_type = self.get_type()
        if problem_type in (ProblemType.MCQ, ProblemType.CHOOSE_ALL):
            self.input_mcq(answer_list)
        elif problem_type == ProblemType.FITB:
            self.input_fitb(answer_list)
        elif problem_type == ProblemType.INPUT:
            self.input_input(answer_list)

    def input_mcq(self, answer_list: list):
        for number in answer_list:
            time.sleep(0.25)
            choice = self.page.query_selector(queries.mcq_string(number))
            choice.click()
        time.sleep(0.25)
        self.submit()

    def input_fitb(self, answer_list: list):
        toggles = self.page.query_selector_all('.o-menu.fitb-menu-container')
        for i, button, in enumerate(toggles):
            button.click()
            time.sleep(0.2)
            choice = button.query_selector_all('.o-menu__item')[answer_list[i]]
            choice.click()
            time.sleep(0.1)

    def input_input(self, answer_list: list):
        self.page.fill(queries.INPUT_QUESTION_BOX, answer_list[0])
        self.submit()

    def submit(self):
        submit = self.page.query_selector(queries.SUBMIT_ANSWERS)
        submit.click()

    def move_on(self):
        letsgo_button = self.page.query_selector(queries.MOVE_ONA)
        next_button = self.page.query_selector(queries.MOVE_ONB)
        if letsgo_button:
            letsgo_button.click()
        elif next_button:
            next_button.click()
