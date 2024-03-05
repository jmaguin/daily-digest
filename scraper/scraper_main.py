#file: scaper_main.py
import sys
from bs4 import BeautifulSoup
from scraper.Ap import Ap
from scraper.Npr import Npr
from scraper.Cnn import Cnn
from scraper.PbsNewshour import PbsNewshour
sys.path.append("../database")
from database import Database

print("Program running!\n")

# master list of tags in config.py

# Instantiate database
db = Database()

# Add PBS Newshour articles to database
pbs_newshour = PbsNewshour()
for article in pbs_newshour.articles:
    db.insert_article(article)

# Add NPR articles to database
npr = Npr()
for article in npr.articles:
    # Keep tag names consistent. (PBS uses "nation")
    if(article.tag == "national"):
        article.tag = "nation"
    db.insert_article(article)

# Add AP articles to database
ap = Ap()
for article in ap.articles:
    # Keep tag names consistent
    if(article.tag == "world-news"):
        article.tag = "world"
    elif(article.tag == "climate-and-environment"):
        article.tag = "climate"
    elif(article.tag == "us-news"):
        article.tag = "nation"
    db.insert_article(article)

# Add Cnn articles to database
cnn = Cnn()
for article in cnn.articles:
    # Keep tag names consistent
    if(article.tag == "us"):
        article.tag = "nation"
    db.insert_article(article)
