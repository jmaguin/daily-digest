from pyscript import document, window
from pyweb import pydom
import config
import local_storage
from Article import *

# list of articles selected on index.html (Article objects)
selected_articles = local_storage.retrieve_articles()
if len(selected_articles) == 0:
    local_storage.clear_local_storage()     # clear localStorage
    window.location.href = "index.html" # redirect back to home page

summary = local_storage.retrieve_articles_summary()     # get summary generated in loading.py

tags = document.querySelector(".tags")      # select <ul> list of tags
# Create list of tags based off article sources
for article in selected_articles:           
    tag = document.createElement("li")
    tag.innerText = article.tag.capitalize()
    tags.append(tag)

article_tag = document.querySelector("article")     # select article tag
paragraph_tag = document.createElement("p")         # create paragraph tag
paragraph_tag.innerText = summary 
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

local_storage.clear_local_storage()     # clear localStorage
