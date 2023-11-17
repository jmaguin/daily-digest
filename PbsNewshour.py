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
        self.tags = ["politics", "arts", "economy", "science", "health", "education"]    # all tags for PBS

        # Build list of all relevant articles
        # Key: tag name     Value: List of articles
        self.articles = {}
        for tag in self.tags:
            page = requests.get(baseURL + tag)                  # get page
            soup = BeautifulSoup(page.content, "html.parser")   # soupify
            
            # Grab links to all articles from current tag/category
            # links_set: Type ResultSet
            links_set = soup.find_all("a", class_=["home-hero__title", "card-xl__title", "card-md__title",
                                                      "card-sm__title", "card-horiz__title", "card-thumb__link"])
            
            # Retrieve articles from links_set
            # Add articles to self.articles
            temp_list = []
            for link in links_set:
                page = requests.get(link["href"])
                soup = BeautifulSoup(page.content, "html.parser")
                temp_list.append(soup)
            
            self.articles[tag] = temp_list
            temp_list.clear()

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
    # Key: tag      Value: articles
    def print_articles(self):
        for tag in self.articles:
            print("------------" + "TAG: " + tag + "------------")
            for article in self.articles[tag]:
                print(article.prettify())