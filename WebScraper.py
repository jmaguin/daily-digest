#file WebScraper.py

from abc import ABC, abstractmethod;

# Abstract class for a web scraper. Serves as a template for all scrapers for different sites
class WebScraper(ABC):

    # Initialize object
    # Define tags to collect data for
    # Get pages for each tag/category
    # Get articles from each page
    @abstractmethod
    def __init__(self):
        pass

    # Retrieve all information about article from its URL
    # Returns Article oject
    # Returns None if fails
    @abstractmethod
    def create_article(self, tag, url):
        pass

    # Print found articles
    @abstractmethod
    def print_articles(self):
        pass