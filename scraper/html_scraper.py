from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
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

    def login(self):
        """Logs into albert via .env credentials."""
        self.page.fill('[data-testid="log-in--identifier"]', config.ALBERT_EMAIL)    
        self.page.fill('[data-testid="log-in--password"]', config.ALBERT_PASSWORD)
        time.sleep(0.5)
        self.page.click('[type="submit"]')

    def skip_tour(self):
        """Checks for tour and skips it."""
        skip = self.page.query_selector(queries.TOUR_BUTTON)
        if skip:
            skip.click()
    
    def get_type(self):
        """Gets the question type."""
        for problem_type, query in queries.PROBLEM_TYPE_QUERIES:
            if self.page.query_selector(query) is not None:
                return problem_type
        return None