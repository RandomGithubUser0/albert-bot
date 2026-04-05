from playwright.sync_api import sync_playwright
from playwright.sync_api import Browser
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError
from enums import ProblemType
from scraper import queries

import config
import json
import re
import string
import time
import utils

class Scraper:
    """test"""
    page : Page 
    browser : Browser
    
    def __init__(self, page : Page, browser : Browser):
        """Constructor to initialize scraper."""
        self.page = page
        self.browser = browser

    def login(self):
        """Logs into albert via .env credentials."""
        self.page.goto("https://www.albert.io/log-in")
        self.page.fill(queries.LOGIN_IDENTIFIER, config.ALBERT_EMAIL)    
        self.page.fill(queries.LOGIN_PASSWORD, config.ALBERT_PASSWORD)
        time.sleep(0.5)
        self.page.click(queries.LOGIN_BUTTON)
    
    def get_type(self) -> ProblemType:
        """Gets the question type."""
        for problem_type, query in queries.PROBLEM_TYPE_QUERIES.items():
            if self.page.query_selector(query) is not None:
                return problem_type
        return None
    
    def setup_page(self, url : string):
        """Sets up the page"""
        self.page.goto(url)
        try:
            skip = self.page.wait_for_selector(queries.TOUR_BUTTON, timeout=1000)
            skip.click()
        except TimeoutError:
            print("Tour button didn't show up, skipping...")

    def albert_is_completed(self) -> bool:
        achieved_advanced = self.page.query_selector(':text("You achieved \\"Advanced\\" on this skill level!")')
        reached_advanced = self.page.query_selector(':text("You achieved \\"Advanced\\" on this skill level!")')
        return (achieved_advanced is not None) or (reached_advanced is not None) 

    def parse_question(self) -> list:
        """Parses current albert.io into a content-based prompt."""
        problem_type = self.get_type()
        if (problem_type == ProblemType.MCQ) or (problem_type == ProblemType.CHOOSE_ALL):
            return self.parse_mcq()
        elif (problem_type == ProblemType.FITB):
            return self.parse_fitb()
        elif (problem_type == ProblemType.INPUT):
            return self.parse_input()
        else:
            return []

        # MCQ and CHOOSE_ALL will use the same parser
        # FITB Parser
        # INPUT Parser

    def parse_mcq(self):
        # Extract question
        content = [{"type": "text", "text": "|| Math question: ||"}]
        question = self.page.query_selector(".question-wrapper__body")

        question_paragraphs = question.query_selector_all(".paragraph")
        if question_paragraphs:
            text = "\n".join(utils.clean_inner_text(p.inner_text()) for p in question_paragraphs)
            content.append({"type": "text", "text": text})

        question_image = question.query_selector(".image-supplement__image")
        if question_image:
            src = question_image.get_attribute("src")
            content.append({"type": "image", "data": utils.fetch_image_b64(src, self.browser)})

        content.append({"type": "text", "text": "|| Answer Choices: ||"})

        # Extract MCQ choices
        i = 0 
        while True:
            option = self.page.query_selector(queries.mcq_string(i))
            if option is None:
                break

            content.append({"type": "text", "text": f"Answer choice {i}:"})

            option_text = option.query_selector(".paragraph")
            if option_text:
                content.append({ "type": "text", "text": utils.clean_inner_text(option_text.inner_text())})

            option_image = option.query_selector(".image-supplement__image")
            if option_image:
                src = option_image.get_attribute("src")
                content.append({"type": "image", "data": utils.fetch_image_b64(src, self.browser)})

            i += 1

        return content   


        

    # def parse_fitb(self):

    # def parse_input(self):

    # def extract_fitb_choices(self):
