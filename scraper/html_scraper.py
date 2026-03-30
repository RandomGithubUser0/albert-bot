from playwright.sync_api import sync_playwright
from playwright.sync_api import Page
from enums import SolverType, ProblemType

import json
import re
import string

class Scraper:
    """test"""
    lol = "e"  # Class attribute

    def __init__(self, name, age):
        """Constructor to initialize instance attributes."""
        self.name = name  # Instance attribute
        self.age = age    # Instance attribute

    def description(self):
        """An instance method to get the dog's description."""
        return "67"