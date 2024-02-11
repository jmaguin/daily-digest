# file: cnnUnderscoredTest.py
# I made this to find out why the title could not be found from cnn underscored articles
# Result: Found out that Cnn underscored makes the scraper do a captcha

import sys
from bs4 import BeautifulSoup
from CnnUnderscored import CnnUnderscored


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

# Add Cnn articles to database
cnnUnderscored = CnnUnderscored()
for article in cnnUnderscored.articles:
    # Keep tag names consistent
    if(article.tag == "us"):
        article.tag = "nation"
