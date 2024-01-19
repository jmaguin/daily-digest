#file: main.py
import sys
from bs4 import BeautifulSoup
from Npr import Npr
from PbsNewshour import PbsNewshour
sys.path.insert(1, "../database")
from Database import Database

print("Program running!\n")

# Instantiate database
db = Database()

# Instantiate scrapers
# pbs_newshour = PbsNewshour()
npr = Npr()
# ap = Ap()

# Add PBS Newshour articles to database
# for article in pbs_newshour.articles:
    # db.insert_article(article)

# Add NPR articles to database
for article in npr.articles:
    # Keep tag names consistent. (PBS uses "nation")
    if(article.tag == "national"):
        article.tag == "nation"
    db.insert_article(article)

# Add AP articles to database
# tags = ap.get_tags()
# add_articles_to_db("Associated Press", ap.get_articles())

