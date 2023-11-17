import requests
from WebScraper import WebScraper
from bs4 import BeautifulSoup

# Class to gather data from Pbs NewsHour
# Base URL: https://www.pbs.org/newshour/
class PbsNewshour(WebScraper):

    # Initialize the object
    def __init__(self):
        baseURL = "https://www.pbs.org/newshour/"
        self.tags = ["politics", "arts", "economy", "science", "health", "education"]    # all tags for PBS

        # Build list of all relevant articles
        # Key: tag name     Value: ResultSet of articles
        self.articles = {}
        for tag in self.tags:
            page = requests.get(baseURL + tag)                  # get page
            soup = BeautifulSoup(page.content, "html.parser")   # soupify
            
            # Grab all articles from current tag/category
            # articles_set: Type ResultSet
            articles_set = soup.find_all("article", class_=["card-xl", "card-lg", "card-horiz"])

            self.articles[tag] = articles_set   # add articles to dictionary

    # Returns List of all articles gathered by scraper
    # Used to place articles into database
    def get_articles(self):
        # Iterate through all tags
        return self.articles
    
    # Returns List of all tags/categories from site
    def get_tags(self):
        return self.tags

    # Print out all found articles
    # Key: tag      Value: articles
    def print_articles(self):
        for tag in self.articles:
            print("------------" + "TAG: " + tag + "------------")
            for article in self.articles[tag]:
                print(article.prettify())