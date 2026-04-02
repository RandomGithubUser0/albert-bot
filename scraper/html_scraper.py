from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from enums import SolverType, ProblemType
from scraper import queries

import json
import re
import string

class Scraper:
    """test"""
    page : Page  # Class attribute
    
    def __init__(self, page : Page):
        """Constructor to initialize scraper."""

    def skip_tour(self):
        """Checks for tour and skips it."""
        skip = self.page.query_selector(queries.TOUR_BUTTON)
        if skip:
            skip.click()
    
    