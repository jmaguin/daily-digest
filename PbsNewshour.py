#file: PbsNewshour.py
import requests
from bs4 import BeautifulSoup
from ProgressBar import ProgressBar
from WebScraper import WebScraper


# Class to gather data from Pbs NewsHour
# Base URL: https://www.pbs.org/newshour/
class PbsNewshour(WebScraper):

    # Initialize the object
    def __init__(self):
        print("PBS Scraper Started.\n")
        baseURL = "https://www.pbs.org/newshour/"
        page_range = 1 # how many pages to get articles from

        # Dictionary of all articles
        # Key: tag name     Value: List of articles in soup form
        self.articles = {"politics": [],
                         "arts": [],
                         "economy": [],
                         "science": [],
                         "health": [],
                         "education": [],
                         "world": [],
                         "nation": []
                        }     # all tags for PBS

        self.tags = list(self.articles.keys())

        # Build list of all relevant articles
        for tag in self.tags:
            art_count = 0   # num of articles found for this tag
            prog_bar = ProgressBar(page_range)

            # Get articles from pages 1 - page_range
            for page_num in range(1, page_range+1):
                page_num_base = "/page/"
                tag_home_page = requests.get(baseURL + tag + page_num_base + str(page_num)) # get page
                tag_home_soup = BeautifulSoup(tag_home_page.content, "html.parser")         # soupify

                # Grab links to all articles from current tag/category
                # links_set: Type ResultSet
                links_set = tag_home_soup.find_all("a", class_=["home-hero__title", "card-xl__title", "card-lg__title",
                                                        "card-lg__title card-lg__title--with-space", "card-md__title",
                                                        "card-sm__title", "card-horiz__title", "card-thumb__link"])
                
                # Retrieve articles from links_set
                # Add articles to self.articles
                for link in links_set:
                    link_page = requests.get(link["href"])
                    link_soup = BeautifulSoup(link_page.content, "html.parser")
                    self.articles[tag].append(link_soup)
                    art_count+=1
                
                prog_bar.update_progress()

            print("\nSOURCE: PBS | TAG: " + tag + " | ARTICLES LOGGED: " + str(art_count) + "\n")
            break

    # Returns List of all articles (soup form)
    # Used to place articles into database
    def get_articles(self):
        return self.articles
    
    # Returns List of all tags/categories from site
    def get_tags(self):
        return self.tags

    # Print out all found articles
    def print_articles(self):
        for tag in self.tags:
            count = 1
            print("\n------------ " + "TAG: " + tag + " ------------\n")
            for article in self.articles[tag]:
                print("(" + str(count) + ") " + article.find("h1").get_text())
                count+=1