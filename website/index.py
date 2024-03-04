import dateutil.parser
import datetime
from pyscript import document
from pyweb import pydom
import config
import sqlite3
import sys
sys.path.insert(1, "../database")
from Database import Database

# Color palette -> from index.css
gray = "#444444"
dark_gray = "#313131"
darkest_gray = "#292929"
text_color = "#c0c0c0"
accent_color = "#58a858"
dark_accent_color = "#438143"
darkest_accent_color = "#346634"

all_articles = []   # all articles for current topic


# populate the dropdown with topics
dropdown_element = document.getElementById("dropdown")  # find dropdown element
for topic in config.master_tags:
    new_option = document.createElement("option")   # create option element
    new_option.value = topic
    new_option.setAttribute("py-click", "dropdown_clicked")
    new_option.innerText = topic.capitalize()
    dropdown_element.append(new_option) # append to DOM

# intitialize article counter
article_count = document.querySelector(".articleCount")
article_count.innerText = "Articles Selected: 0/" + str(config.max_selection)

# Instantiate database
db = Database()

def process_date(article):
    source = article[2]
    raw_date = article[3]

    # format: Published 9:23 AM EST, Mon February 12, 2024
    if source == "CNN":
        date_list = raw_date.split()    # split into words
        raw_date = ""
        i = 0
        for word in reversed(date_list):    # only get last 3 words
            raw_date = raw_date + " " + word
            i = i + 1
            if i > 2:
                break
        date = dateutil.parser.parse(raw_date)

    # format: Unix epoch
    elif source == "AP":
        date_int = int(raw_date)/1000       # convert from str to int & from ms to sec
        date = datetime.datetime.fromtimestamp(date_int)
    
    # formats: 2024-01-16T20:37:02-05:00 or Jan 13, 2024 5:30 PM EST
    # PBS has 2 different date formats
    elif source == "NPR" or source == "PBS Newshour":
        raw_date = raw_date.replace("EST", "")      # remove EST -> causes time zone error?
        split_loc = raw_date.find("T")      # find "T"
        if split_loc != -1:
            raw_date = raw_date[:split_loc]     # cut off string after "T" to just get date
        date = dateutil.parser.parse(raw_date)

    return str(date.strftime("%b %d, %Y"))

# refresh displayed articles based on topic
def refresh_articles():
    articles_list = db.get_articles(config.selected_topic)
    main_element = document.querySelector("main")   # select <main>
    main_element.innerHTML = ""     # clear main

    # append retrieved articles to main
    i = 0
    for article in articles_list:
        # create article
        new_article = document.createElement("article")
        new_article.setAttribute("py-click", "article_clicked")

        # create <h3> header
        new_header = document.createElement("h3")

        # create <a> link
        new_link = document.createElement("a")      # create link
        new_link.href = article[4]                  # set link attribute
        new_link.target = "_blank"                  # open in new tab
        new_link.innerText = article[1].title()     # set title

        # create <ul> for tags
        new_tags = document.createElement("ul")             # create tags list
        new_tags.classList.add("tags")                      # add 'tags' class
        new_tag = document.createElement("li")              # create tag
        new_tag.innerText = process_date(article)

        new_text = document.createElement("p")          # create paragraph
        new_text.innerText = article[5][:250] + "..."   # add text blurb (250 char limit)

        new_header.append(new_link)                 # place <a> into <h3>
        new_article.append(new_header)              # place <h3> into <article>
        new_tags.append(new_tag)                    # place <li> into <ul>
        new_article.append(new_tags)                # place <ul> into <article>
        new_article.append(new_text)                # place <p> into <article>
        main_element.append(new_article)            # append new article to <main>

        for selected_article in config.selected_articles:
            url = selected_article.querySelector("a").href
            if(url == article[4]):
                new_article.style.backgroundColor = darkest_gray

        i = i + 1
        if(i > 10):
            break

refresh_articles()

# called when generate button clicked
def generate(event):
    print("generate!")

# called when new dropdown item selected
def dropdown_clicked(event):
    config.selected_topic = event.target.value
    refresh_articles()

# called when article clicked
def article_clicked(event):
    this_article = event.currentTarget
    
    # iterate thru selected_articles
    # check to see if already clicked
    this_url = this_article.querySelector("a").href
    for that_article in config.selected_articles:
        that_url = that_article.querySelector("a").href

        # article has already been clicked
        if this_url == that_url:
            config.selected_articles.remove(that_article)
            this_article.style.backgroundColor = gray
            # update article counter
            article_count.innerHTML = "Articles Selected: " + str(len(config.selected_articles)) + "/" + str(config.max_selection)
            return

    # if num of selected articles lower than max allowed
    if len(config.selected_articles) < config.max_selection:
        config.selected_articles.append(this_article)
        this_article.style.backgroundColor = darkest_gray
    
    # update article counter
    article_count.innerHTML = "Articles Selected: " + str(len(config.selected_articles)) + "/" + str(config.max_selection)
    

