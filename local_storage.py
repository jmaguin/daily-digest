from js import localStorage
from pyweb import pydom
from Article import *

# This file contains functions to aid in storing and retrieving articles from localStorage.

num_of_articles_key = "num_of_articles"  # key of localStorage value with total number of articles saved
articles_summary_key = "articles_summary"   # key of localStorage value with summary of all articles

# Parameters: list of Article objects to be saved in localStorage
def save_articles(articles_list):
    # Ensure elements in list
    if len(articles_list) == 0:
        return

    # Save important contextual info to be used by next page
    localStorage.setItem(num_of_articles_key, str(len(articles_list)))    # holds number of selected articles
    # Iterate thru articles and save to localStorage
    # i starts at 0
    for i, article in enumerate(articles_list):
        # Save tag
        tag_key = "tag" + str(i)
        localStorage.setItem(tag_key, article.tag)
        # Save title
        title_key = "title" + str(i)
        localStorage.setItem(title_key, article.title)
        # Save Source
        source_key = "source" + str(i)
        localStorage.setItem(source_key, article.source)
        # Save Date
        date_key = "date" + str(i)
        localStorage.setItem(date_key, article.date)
        # Save URL
        url_key = "url" + str(i)
        localStorage.setItem(url_key, article.url)
        # Save content
        content_key = "content" + str(i)
        localStorage.setItem(content_key, article.content)

# Return value: list of Article objects saved in localStorage
def retrieve_articles():
    num_of_articles = int(localStorage.getItem(num_of_articles_key))     # get num of saved articles
    if num_of_articles == 0:
        return
    
    # Iterate thru localStorage and build list of Article objects
    articles_list = []
    for i in range(num_of_articles):
        # Retrieve current article's info
        tag = localStorage.getItem("tag" + str(i))
        title = localStorage.getItem("title" + str(i))
        source = localStorage.getItem("source" + str(i))
        date = localStorage.getItem("date" + str(i))
        url = localStorage.getItem("url" + str(i))
        content = localStorage.getItem("content" + str(i))

        # Create Article object and append to list
        articles_list.append(Article(tag, title, source, date, url, content))

    return articles_list

# Save articles summary as generated by LLM
# Parameter: summary string
def save_articles_summary(summary):
    localStorage.setItem(articles_summary_key, summary)

# Return summary
def retrieve_articles_summary():
    return localStorage.getItem(articles_summary_key)

# Clears all items in localStorage
def clear_local_storage():
    localStorage.clear()