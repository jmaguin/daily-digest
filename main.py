#file: main.py
import warnings
from bs4 import BeautifulSoup
from Database import Database
from PbsNewshour import PbsNewshour

print("Program running!\n")

# Instantiate database
db = Database()

# Instantiate scrapers
pbs_newshour = PbsNewshour()
pbs_newshour.print_articles()
# npr = Npr()
# ap = Ap()

# Adds articles to the database
    # Parameters
        # source: String. source name
        # data: Dictionary. values = list of articles (soup form), keys = tags
def add_articles_to_db(source, data):
    # iterate thru all tags & articles
    for tag in data:
        for article in data[tag]:
            # If source is PBS
            if source == "PBS Newshour":
                art_title = article.find("h1").get_text()

                # get date
                try: 
                    date = article.find("time")
                    date = date["content"]  # date found from normal article
                except KeyError:
                    date = article.find("time").get_text() # date found from show
                except Exception as e:
                    warnings.warn("WARNING: Could not locate article date.\n\tArticle: %s\n\tError: %s" % (art_title, e))
                    continue    # unforseen issue

                # get content
                try:
                    content = article.find("div", class_=["body-text"]).get_text()  # text from normal article
                except KeyError:
                    content = article.find("div", class_=["vt__excerpt body-text"]).get_text()  # text excerpt from show
                except Exception as e:
                    warnings.warn("WARNING: Could not locate article content.\n\tArticle: %s\n\tError: %s" % (art_title, e))
                    continue    # can't find text - skip
                    
                # get URL
                try:
                    url = article.find("meta", {"property": "og:url"})["content"]     # URL found
                except Exception as e:
                    warnings.warn("WARNING: Could not locate article URL.\n\tArticle: %s\n\tError: %s" % (art_title, e))
                    url = ""    # can't find URL

            # If source is NPR
            elif source == "NPR":
                pass
            
            # If source is Associated Press
            elif source == "Associated Press":
                pass

            db.insert_article(source, tag, date, url, content)  # order of parameters important

# Add PBS articles to database
tags = pbs_newshour.get_tags()
add_articles_to_db("PBS Newshour", pbs_newshour.get_articles())

# Add NPR articles to database
# tags = npr.get_tags()
# add_articles_to_db("NPR", npr.get_articles())

# Add AP articles to database
# tags = ap.get_tags()
# add_articles_to_db("Associated Press", ap.get_articles())

