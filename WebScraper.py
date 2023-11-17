#file abstract.py

from abc import ABC, abstractmethod;

# Abstract class for a web scraper. Serves as a template for all scrapers for different sites
class WebScraper(ABC):

    # Initialize object
    # Define tags/categories to collect data for
    # Get pages for each tag/category
    # Get articles from each page
    @abstractmethod
    def __init__(self):
        pass

    # Returns List of all articles gathered by scraper
    # Used to place articles into database
    @abstractmethod
    def get_articles(self):
        pass

    # Returns List of all tags/categories from site
    @abstractmethod
    def get_tags(self):
        pass

    # Print found articles' titles & tags
    @abstractmethod
    def print_articles(self):
        pass