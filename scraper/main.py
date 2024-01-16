#file: main.py
from bs4 import BeautifulSoup
from Database import Database
from PbsNewshour import PbsNewshour

print("Program running!\n")

# Instantiate database
db = Database()

# Instantiate scrapers
pbs_newshour = PbsNewshour()
# npr = Npr()
# ap = Ap()

# Add PBS Newshour articles to database
for article in pbs_newshour.articles:
    db.insert_article(article)

# Add NPR articles to database
# tags = npr.get_tags()
# add_articles_to_db("NPR", npr.get_articles())

# Add AP articles to database
# tags = ap.get_tags()
# add_articles_to_db("Associated Press", ap.get_articles())

