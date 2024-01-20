#file: main.py
import sys
from Ap import Ap
from bs4 import BeautifulSoup
from Npr import Npr
from PbsNewshour import PbsNewshour
sys.path.insert(1, "../database")
from Database import Database

print("Program running!\n")

# master list of all tags
master_tags = ["politics",
                "world",
                "sports",
                "entertainment",
                "business",
                "science",
                "health",
                "climate",
                "technology",
                "religion",
                "nation",
                "arts",
                "economy",
                "education",
                "race",
                "culture",
                "movies",
                "food",
                "gaming",
                "television"
                ]

# Instantiate database
db = Database()

# Instantiate scrapers
pbs_newshour = PbsNewshour()
npr = Npr()
ap = Ap()

# Add PBS Newshour articles to database
for article in pbs_newshour.articles:
    db.insert_article(article)

# Add NPR articles to database
for article in npr.articles:
    # Keep tag names consistent. (PBS uses "nation")
    if(article.tag == "national"):
        article.tag = "nation"
    db.insert_article(article)

# Add AP articles to database
for article in ap.articles:
    # Keep tag names consistent
    if(article.tag == "world-news"):
        article.tag = "world"
    elif(article.tag == "climate-and-environment"):
        article.tag = "climate"
    elif(article.tag == "us-news"):
        article.tag = "nation"
    db.insert_article(article)

