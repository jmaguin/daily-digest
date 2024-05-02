from pyscript import document, window
from pyweb import pydom
from js import localStorage
import config
from Database import *
from Article import *

# Color palette -> from index.css
gray = "#444444"
dark_gray = "#313131"
darkest_gray = "#292929"
text_color = "#c0c0c0"
accent_color = "#58a858"
dark_accent_color = "#438143"
darkest_accent_color = "#346634"

# Retrieve articles & text summary from localStorage
selected_articles = []  # list of articles selected on index.html (Article objects)
articles_summary = ""        # summary generated by the LLM in loading.py

# Begin connection to database
db = Database()

num_of_urls_string = localStorage.getItem(config.localStorage_lenth_key)   # get all selected articles using URLs from localStorage
articles_summary = localStorage.getItem(config.localStorage_summary_key)  # get summary generated by LLM
num_of_urls = 0

# if num_of_urls is not in local storage do not try to get the urls

# Check if num_of_urls_string is NoneType
if num_of_urls_string is not None:  # check to avoid calling int() on NoneType
    num_of_urls = int(num_of_urls)

if int(num_of_urls) == 0:
    print("localStorage_length_key not found.")
    localStorage.clear()    # clear the localStorage
    window.location.href = "index.html" # redirect back to home page
else:
    # loop and add Article objects to selected_articles
    for i in range(num_of_urls):
        url = localStorage.getItem("url" + str(i))  # retrieve url from localStorage
        this_article = db.get_article(url)  # turn URL into Article object

        # ensure article was found
        if this_article is None:
            print("Article could not be located in database.\nURL: " + url)
        else:
            selected_articles.append(this_article)

tags = document.querySelector(".tags")      # select <ul> list of tags
# Create list of tags based off article sources
for article in selected_articles:           
    tag = document.createElement("li")
    tag.innerText = article.source
    tags.append(tag)

article_tag = document.querySelector("article")     # select article tag
paragraph_tag = document.createElement("p")         # create paragraph tag
paragraph_tag.innerText = articles_summary 
article_tag.append(paragraph_tag)                   # add LLM summary to webpage

citations = document.querySelector(".citations")     # select UL that contains citations
# add citation for each article used in summary
for article in selected_articles:
    # create <a> link
    new_list_item = document.createElement("li")
    new_link = document.createElement("a")      # create link
    new_link.href = article.url                 # set link attribute
    new_link.target = "_blank"                  # open in new tab
    new_link.innerText = article.title.strip()  # set title

    new_list_item.append(new_link)
    citations.append(new_list_item)             # add new citation to UL

# clear relevant localStorage
localStorage.removeItem("num_of_urls")    
for i in range(num_of_urls):
    url = localStorage.removeItem("url" + str(i))  # retrieve url from localStorage
