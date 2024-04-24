#file: Npr.py
import dateutil
import requests
import time
import sys
import warnings
import string
from bs4 import BeautifulSoup
from scraper.ProgressBar import ProgressBar
from scraper.WebScraper import WebScraper
sys.path.append("../daily_digest/Article")
from Article import *


# Class to gather data from NPR
# Base URL: https://www.npr.org/
class Npr(WebScraper):

    # Initialize the object
    def __init__(self):
        print("/--------------- NPR scraper started. ---------------/")
        baseURL = "https://www.npr.org/sections/"
        page_range = 1 # how many pages to get articles from
        
        # List of all tags for NPR
        self.tags = ["national",
                     "world",
                     "politics",
                     "business",
                     "health",
                     "science",
                     "climate",
                     "race",
                     "culture",
                     "movies",
                     "food",
                     "gaming",
                     "television"
                    ] 

        # List of all articles from NPR
        self.articles = []

        self.source_name = "NPR"
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
            header_tags = tag_home_soup.find_all("h2")
            for header in header_tags:
                a_tag = header.find("a")
                if a_tag:
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
        print("\n\nSOURCE: NPR | ELAPSED TIME: %dsec | ARTICLES LOGGED: %d\n" % (end-start, self.art_count))
        print("/--------------- NPR scraper completed. ---------------/")
        

    # Retrieve all information about article from its URL
    # Returns Article object -> None if fails
    def create_article(self, tag, url):
        req = requests.get(url)   # generate URL
        soup = BeautifulSoup(req.content, "html.parser")  # create soup from URL

        # get title
        try:
            title = string.capwords(soup.find("h1").get_text())
        except Exception as e:
            warnings.warn("\nWARNING: Could not locate article title.\n\tArticle: %s\n\tError: %s" % (url, e))
            return None

        # get date
        try: 
            date_block = soup.find("div", class_="dateblock")
            time_tag = date_block.find("time")
            date = time_tag["datetime"]
        except Exception as e:
            warnings.warn("\nWARNING: Could not locate article date.\n\tArticle: %s\n\tError: %s" % (url, e))
            return None

        # get content
        try:
            storytext = soup.find("div", class_="storytext")
            p_tags = storytext.find_all("p", recursive=False)    # filter to remove image caption, etc.
            content = ""

            # assemble all paragraphs into single string
            for p in p_tags:
                content += p.get_text()
        except Exception as e:
            warnings.warn("\nWARNING: Could not locate article content.\n\tArticle: %s\n\tError: %s" % (url, e))
            return None

        return Article(tag, title, self.source_name, self.reformat_date(date), url, content)

    # Print out all found articles
    def print_articles(self):
        for tag in self.tags:
            count = 1
            print("\n------------ " + "TAG: " + tag + " ------------\n")
            for article in self.articles:
                if (article.tag == tag):
                    print("(" + str(count) + ") " + article.title)
                    count+=1

    # Publication dates from different sources are in different formats
    # This function converts all of them to MON DD, YYYY
    # Input: Raw date String
    # Output: Properly formatted date string
    def reformat_date(self, raw_date):
        raw_date = raw_date.replace("EST", "")      # remove EST -> causes time zone error?
        split_loc = raw_date.find("T")              # find "T"
        if split_loc != -1:
            raw_date = raw_date[:split_loc]     # cut off string after "T" to just get date
        date = dateutil.parser.parse(raw_date)

        return str(date.strftime("%b %d, %Y"))