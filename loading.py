from js import localStorage
from pyscript import document
from pyweb import pydom
from Database import *
import config

# Color palette -> from index.css
gray = "#444444"
dark_gray = "#313131"
darkest_gray = "#292929"
text_color = "#c0c0c0"
accent_color = "#58a858"
dark_accent_color = "#438143"
darkest_accent_color = "#346634"

selected_articles = []  # list of articles selected on index.html

# Instantiate database
db = Database()

# get all selected articles using URLs from localStorage
num_of_urls = localStorage.getItem(config.localStorage_lenth_key)

# if num_of_urls is not in local storage do not try to get the urls

# this check is needed to prevent an error message from showing up
if(num_of_urls is None):
    print("localStorage_length_key not found")
else:
    for i in range(int(num_of_urls)):
        url = localStorage.getItem("url" + str(i))
        print(url)
        selected_articles.append(db.get_article(url))

localStorage.clear()    # clear the localStorage

# LLM Code here ------------------------------------------->




# ------------------------------------------------------------<

