#file: Ap.py
import requests
import time
import warnings
from Article import Article
from bs4 import BeautifulSoup
from ProgressBar import ProgressBar
from WebScraper import WebScraper


# Class to gather data from AP
# Base URL: https://apnews.com/
class Ap(WebScraper):

    # Initialize the object
    def __init__(self):
        print("/--------------- AP scraper started. ---------------/")
        baseURL = "https://apnews.com/"
        page_range = 1 # how many pages to get articles from
        
        # List of all tags for AP
        self.tags = ["politics",
                     "world-news",
                     "sports",
                     "entertainment",
                     "business",
                     "science",
                     "health",
                     "climate-and-environment",
                     "technology",
                     "religion",
                     "us-news"
                    ] 

        # List of all articles from AP
        self.articles = []

        self.source_name = "AP"
        self.art_count = 0   # num of articles found for this tag
        
        start = time.time()
        # Build list of all relevant articles
        for tag in self.tags:
            prog_bar = ProgressBar(page_range, tag)

            # Get articles
            tag_home_page = requests.get(baseURL + tag) # get page
            tag_home_soup = BeautifulSoup(tag_home_page.content, "html.parser")         # soupify

            # Grab links to all articles from current tag on current page
            # header_tags: Type ResultSet
            links_set = set()
            header_tags = tag_home_soup.find_all("h3", class_="PagePromo-title")
            for header in header_tags:
                a_tag = header.find("a")
                if a_tag:
                    if ("/video/" not in a_tag["href"]) and ("/features/" not in a_tag["href"]):  # only log articles, not videos
                        links_set.add(a_tag)
            
            # Retrieve articles from links_set
            # Add articles to self.articles
            for link in links_set:
                article = self.create_article(tag, link["href"])    # create Article object
                if article is not None:
                    self.articles.append(article)   # append Article to list
                    self.art_count+=1
            
            prog_bar.update_progress()
        
        end = time.time()
        print("\n\nSOURCE: AP | ELAPSED TIME: %dsec | ARTICLES LOGGED: %d\n" % (end-start, self.art_count))
        print("/--------------- AP scraper completed. ---------------/")
        

    # Retrieve all information about article from its URL
    # Returns Article object -> None if fails
    def create_article(self, tag, url):
        req = requests.get(url)   # generate URL
        soup = BeautifulSoup(req.content, "html.parser")  # create soup from URL

        # get title
        try:
            title = soup.find("h1", class_="Page-headline").get_text()
        except Exception as e:
            warnings.warn("\nWARNING: Could not locate article title.\n\tArticle: %s\n\tError: %s" % (url, e))
            return None

        # get date
        try: 
            date_block = soup.find("div", class_="Page-datePublished")
            if date_block is None:
                date_block = soup.find("div", class_="Page-dateModified")
            time_tag = date_block.find("bsp-timestamp")
            date = time_tag["data-timestamp"]   # format: Unix timestamp
        except Exception as e:
            warnings.warn("\nWARNING: Could not locate article date.\n\tArticle: %s\n\tError: %s" % (url, e))
            return None

        # get content
        try:
            content = soup.find("div", class_="RichTextStoryBody").get_text()
        except Exception as e:
            warnings.warn("\nWARNING: Could not locate article content.\n\tArticle: %s\n\tError: %s" % (url, e))
            return None

        return Article(tag, title, self.source_name, date, url, content)

    # Print out all found articles
    def print_articles(self):
        for tag in self.tags:
            count = 1
            print("\n------------ " + "TAG: " + tag + " ------------\n")
            for article in self.articles:
                if (article.tag == tag):
                    print("(" + str(count) + ") " + article.title)
                    count+=1