#file: Cnn.py
import requests
import time
import warnings
from Article import Article
from bs4 import BeautifulSoup
from ProgressBar import ProgressBar
from WebScraper import WebScraper


# Class to gather data from CNN
# Base URL: https://www.cnn.com/
class Cnn(WebScraper):

    # Initialize the object
    def __init__(self):
        print("/--------------- CNN scraper started. ---------------/")
        baseURL = "https://www.cnn.com/"
        page_range = 1 # how many pages to get articles from
        
        # List of all tags for CNN
        self.tags = ["us",
                     "world",
                     "politics",
                     "business",
                    #  "opinions",
                     "health",
                     "entertainment",
                    #  "style",
                    #  "travel",
                     "sports",
                    ] 

        # List of all articles from CNN
        self.articles = []

        self.source_name = "CNN"
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
            a_tags = tag_home_soup.find_all("a", class_="container__link--type-article")
            for a_tag in a_tags:
                links_set.add(a_tag)

            foundArticle = False
            # Retrieve articles from links_set
            # Add articles to self.articles
            for link in links_set:
                linkPrefix = "https://www.cnn.com"
                href = link["href"]
                # if the link is an ad -> skip it
                if href.startswith("/") == False:
                    continue
                if href.startswith("/cnn-underscored"):
                    continue
                fixedLink = linkPrefix + href
                # warnings.warn("\n%s href" % (href))
                article = self.create_article(tag, fixedLink)    # create Article object
                if article is not None:
                    self.articles.append(article)   # append Article to list
                    self.art_count+=1
                    foundArticle = True
            
            if foundArticle == False:
                warnings.warn("\nWARNING: Could not find articles \n\tTag: %s" % (tag))

            
            prog_bar.update_progress()
        
        end = time.time()
        print("\n\nSOURCE: CNN | ELAPSED TIME: %dsec | ARTICLES LOGGED: %d\n" % (end-start, self.art_count))
        print("/--------------- CNN scraper completed. ---------------/")
        
    @staticmethod
    def formatDate(self, text):
        return text

    # Retrieve all information about article from its URL
    # Returns Article object -> None if fails
    def create_article(self, tag, url):
        try:
            req = requests.get(url)   # generate URL
        except Exception as e:
            warnings.warn("\nWARNING: Could not open connection.\n\tArticle: %s\n\tError: %s" % (url, e))
            return None
        soup = BeautifulSoup(req.content, "html.parser")  # create soup from URL

        # get title
        # TODO: get article title for CNN Underscored pages soup.find(h1) is a NoneType without attribute "get_text"
        try:
            title = soup.h1.get_text()
        except Exception as e:
            warnings.warn("\nWARNING: Could not locate article title.\n\tArticle: %s\n\tError: %s" % (url, e))
            warnings.warn("\n\tsoup.find('h1'): %s" % (soup.find("h1")))
            return None

        # get date
        try: 
            time_date_block = soup.find("div", class_="timestamp")
            time_date_text = time_date_block.get_text()
            date = time_date_text
        except Exception as e:
            warnings.warn("\nWARNING: Could not locate article date.\n\tArticle: %s\n\tError: %s" % (url, e))
            return None

        # get content
        try:
            storytext = soup.find("div", class_="article__content")
            p_tags = storytext.find_all("p", recursive=False)    # filter to remove image caption, etc.
            content = ""

            # assemble all paragraphs into single string
            for p in p_tags:
                content += p.get_text()
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
    