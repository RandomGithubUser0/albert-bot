from playwright.sync_api import Browser, Page, TimeoutError
from enums import ProblemType, CompletionStatus
from scraper import queries
from scraper.parser import Parser

import config
import time
import logger

class Scraper(Parser):
    page: Page
    browser: Browser
    current_url: str

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
        self.current_url = url
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

    def albert_is_completed(self) -> CompletionStatus:
        if self.page.query_selector(queries.ALREADY_COMPLETED_TEXT):
            return CompletionStatus.ALREADY_COMPLETED
        elif self.page.query_selector(queries.JUST_COMPLETED_TEXT):
            return CompletionStatus.JUST_COMPLETED
        return CompletionStatus.NOT_COMPLETED

    def input_answers(self, answer_list: list, problem_type: ProblemType):
        if problem_type in (ProblemType.MCQ, ProblemType.CHOOSE_ALL):
            self.input_mcq(answer_list)
        elif problem_type == ProblemType.FITB:
            self.input_fitb(answer_list)
        elif problem_type == ProblemType.INPUT:
            self.input_input(answer_list)
        self.submit()

    def input_mcq(self, answer_list: list):
        for number in answer_list:
            time.sleep(0.25)
            choice = self.page.query_selector(queries.mcq_string(number))
            choice.click()
        time.sleep(0.25)

    def input_fitb(self, answer_list: list):
        toggles = self.page.query_selector_all(queries.FITB_MENU_CONTAINER)
        for i, button, in enumerate(toggles):
            button.click()
            time.sleep(0.2)
            choice = button.query_selector_all(queries.FITB_MENU_ITEM)[answer_list[i]]
            choice.click()
            time.sleep(0.1)

    def input_input(self, answer_list: list):
        self.page.fill(queries.INPUT_QUESTION_BOX, str(answer_list[0]))

    def submit(self):
        submit = self.page.query_selector(queries.SUBMIT_ANSWERS)
        if submit:
            submit.click()

    def move_on(self):
        for name, query in queries.MOVE_ON_QUERIES.items():
            button = self.page.query_selector(query)
            if not button:
                continue
            button.click()
            if name == "MOVE_ONB":
                logger.log_level_up(self.current_url)
            if name == "MOVE_ONC":
                logger.log_level_down(self.current_url)
            return

        print("Warning: no move_on button found, may loop on same question")


    # For logging
    def get_answer_result(self) -> bool | None:
        """Returns True if correct, False if incorrect, None if not found."""
        if self.page.query_selector('.m-banner__card--positive'):
            return True
        if self.page.query_selector('.m-banner__card--negative'):
            return False
        return None