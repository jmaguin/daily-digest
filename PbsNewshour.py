import requests
from WebScraper import WebScraper
from bs4 import BeautifulSoup

# Class to gather data from Pbs NewsHour
# Base URL: https://www.pbs.org/newshour/
class PbsNewshour(WebScraper):

    # Initialize the object
    def __init__(self, num_of_entries):
        self.CONST_NUM_ENTRIES = num_of_entries   # number of table entries in database
        baseURL = "https://www.pbs.org/newshour/"

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
            tag_home_page = requests.get(baseURL + tag)                  # get page
            tag_home_soup = BeautifulSoup(tag_home_page.content, "html.parser")   # soupify

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

            print("SOURCE: PBS | TAG: " + tag + " | ARTICLES LOGGED: " + str(art_count) + "\n")
            break

    # Returns List of all articles from specified tag gathered by scraper
    # Used to place articles into database
    def get_articles(self, tag):
        # Ensure tag exists in list
        if tag in self.tags:
            num_of_articles = len(self.articles[tag])   # number of articles in specified tag/category

            # Creates list of num_of_articles lists, each with CONST_NUM_ENTRIES items
            # Stores all data for each collected article - source, tag, date, etc.
            article_data = [["" for x in range(self.CONST_NUM_ENTRIES)] for y in range(num_of_articles)]   

            # Iterate thru all articles. Retrieve their data and put them into article_data
            for i in range(num_of_articles):
                # ORDER IMPORTANT
                article_data[i].append("PBS NewsHour")   # Add name of source
                article_data[i].append(tag)              # Add tag

                article_data[i].append(self.articles[tag][i].find("time", class_="post__date")["content"])   # Add the date

                # Add content of article
                # Series of <p> tags
                text = ""
                paragraphs = self.articles[tag][i].find("div", class_="body-text").find_all("p")
                for paragraph in paragraphs:
                    text = text + paragraph.text

                article_data[i].append(text)    # add article body text
        
        # Tag not in list
        else:
            return -1
    
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