from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from playwright.sync_api import TimeoutError
from enums import SolverType, ProblemType
from scraper import queries

import config
import json
import re
import string
import time

class Scraper:
    """test"""
    page : Page  # Class attribute
    
    def __init__(self, page : Page):
        """Constructor to initialize scraper."""
        self.page = page

    def login(self):
        """Logs into albert via .env credentials."""
        self.page.goto("https://www.albert.io/log-in")
        self.page.fill('[data-testid="log-in--identifier"]', config.ALBERT_EMAIL)    
        self.page.fill('[data-testid="log-in--password"]', config.ALBERT_PASSWORD)
        time.sleep(0.5)
        self.page.click('[type="submit"]')
    
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

    def parse_question(self):
        """Parses current albert.io into a prompt."""