#file: PbsNewshour.py
import requests
import time
import warnings
from Article import Article
from bs4 import BeautifulSoup
from ProgressBar import ProgressBar
from WebScraper import WebScraper


# Class to gather data from Pbs NewsHour
# Base URL: https://www.pbs.org/newshour/
class PbsNewshour(WebScraper):

    # Initialize the object
    def __init__(self):
        print("/--------------- PBS Newshour scraper started. ---------------/")
        baseURL = "https://www.pbs.org/newshour/"
        page_range = 10 # how many pages to get articles from
        
        # List of all tags for PBS
        self.tags = ["politics",
                         "arts",
                         "economy",
                         "science",
                         "health",
                         "education",
                         "world",
                         "nation"
                    ] 

        # List of all articles from PBS
        self.articles = []

        self.source_name = "PBS Newshour"
        self.art_count = 0   # num of articles found for this tag
        
        start = time.time()
        # Build list of all relevant articles
        for tag in self.tags:
            prog_bar = ProgressBar(page_range, tag)

            # Get articles from pages 1 - page_range
            for page_num in range(1, page_range+1):
                page_num_base = "/page/"
                tag_home_page = requests.get(baseURL + tag + page_num_base + str(page_num)) # get page
                tag_home_soup = BeautifulSoup(tag_home_page.content, "html.parser")         # soupify

                # Grab links to all articles from current tag on current page
                # links_set: Type ResultSet
                links_set = tag_home_soup.find_all("a", class_=["home-hero__title", "card-xl__title", "card-lg__title",
                                                        "card-lg__title card-lg__title--with-space", "card-md__title",
                                                        "card-sm__title", "card-horiz__title", "card-thumb__link"])
                
                # Retrieve articles from links_set
                # Add articles to self.articles
                for link in links_set:
                    article = self.create_article(tag, link["href"])    # create Article object
                    if article is not None:
                        self.articles.append(article)   # append Article to list
                        self.art_count+=1
                
                prog_bar.update_progress()
        
        end = time.time()
        print("\n\nSOURCE: PBS | ELAPSED TIME: %dsec | ARTICLES LOGGED: %d\n" % (end-start, self.art_count))
        print("/--------------- PBS Newshour scraper completed. ---------------/")
        

    # Retrieve all information about article from its URL
    # Returns Article object -> None if fails
    def create_article(self, tag, url):
        req = requests.get(url)   # generate URL
        soup = BeautifulSoup(req.content, "html.parser")  # create soup from URL

        # get title
        try:
            title = soup.find("h1").get_text()
        except Exception as e:
            warnings.warn("\nWARNING: Could not locate article title.\n\tArticle: %s\n\tError: %s" % (url, e))
            return None

        # get date
        try: 
            date = soup.find("time")
            date = date["content"]  # date found from normal article
        except KeyError:
            date = soup.find("time").get_text() # date found from show
        except Exception as e:
            warnings.warn("\nWARNING: Could not locate article date.\n\tArticle: %s\n\tError: %s" % (url, e))
            return None

        # get content
        try:
            content = soup.find("div", class_="body-text").get_text()  # text from normal article
        except KeyError:
            content = soup.find("div", class_="vt__excerpt body-text").get_text()  # text excerpt from show
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