from pyscript import document
from pyweb import pydom
import config
from Database import *
import sqlite3


# Color palette -> from index.css
gray = "#444444"
dark_gray = "#313131"
darkest_gray = "#292929"
text_color = "#c0c0c0"
accent_color = "#58a858"
dark_accent_color = "#438143"
darkest_accent_color = "#346634"

all_articles = []   # all articles for current topic

# Populate dropdowns in the header -------------------------------------------------

# populate the topics dropdown
topic_dropdown = document.getElementById("topicDropdown")  # find dropdown element
for topic in config.master_tags:
    new_option = document.createElement("option")   # create option element
    new_option.value = topic
    new_option.setAttribute("py-click", "topic_dropdown_clicked")
    new_option.innerText = topic.capitalize()
    topic_dropdown.append(new_option) # append to DOM

# populate the sources dropdown
source_dropdown = document.getElementById("sourceDropdown")  # find dropdown element
for art_source in config.master_sources:
    new_option = document.createElement("option")   # create option element
    new_option.value = art_source
    new_option.setAttribute("py-click", "source_dropdown_clicked")
    new_option.innerText = art_source
    source_dropdown.append(new_option) # append to DOM

# ---------------------------------------------------------------------------------

# intitialize article counter
article_count = document.querySelector(".articleCount")
article_count.innerText = "Articles Selected: 0/" + str(config.max_selection)

# Instantiate database
db = Database()

# Creates an article HTML element
# Input: Article object
# Returns new article
def create_article(article):
    # create article
    new_article = document.createElement("article")
    new_article.setAttribute("py-click", "article_clicked")

    # create <h3> header
    new_header = document.createElement("h3")

    # create <a> link
    new_link = document.createElement("a")      # create link
    new_link.href = article.url                 # set link attribute
    new_link.target = "_blank"                  # open in new tab
    new_link.innerText = article.title.title()  # set title

    # create <ul> for tags
    new_tags = document.createElement("ul")     # create tags list
    new_tags.classList.add("tags")              # add 'tags' class
    new_tag = document.createElement("li")      # create tag for date
    new_tag.innerText = article.date
    another_tag = document.createElement("li")  # create tag for source
    another_tag.innerText = article.source

    new_text = document.createElement("p")      # create paragraph
    new_text.innerText = article.content[:250] + "..."   # add text blurb (250 char limit)

    new_header.append(new_link)                 # place <a> into <h3>
    new_article.append(new_header)              # place <h3> into <article>
    new_tags.append(new_tag)                    # place <li> into <ul>
    new_tags.append(another_tag)                # place <li> into <ul>
    new_article.append(new_tags)                # place <ul> into <article>
    new_article.append(new_text)                # place <p> into <article>

    return new_article

# refresh displayed articles based on topic
def refresh_articles():
    articles_list = db.get_articles(config.selected_topic)
    main_element = document.querySelector("main")   # select <main>
    main_element.innerHTML = ""     # clear main

    # loop through all articles
    i = 0
    for article in articles_list:
        new_article = create_article(article)   # create article

        # pare down articles_list to just ones from specified source (source_dropdown)
        if source_dropdown.value == "All" or source_dropdown.value == article.source:
            main_element.append(new_article)    # append article to <main>

            # re-do all styling for articles that have been selected
            for selected_article in config.selected_articles:
                url = selected_article.querySelector("a").href
                if(url == article.url):
                    new_article.style.backgroundColor = darkest_gray

            i = i + 1
            if(i > 100):
                break

refresh_articles()

# called when generate button clicked
def generate(event):
    print("generate!")

# called when new dropdown item selected
def topic_dropdown_clicked(event):
    config.selected_topic = event.target.value
    refresh_articles()

# called when new dropdown item selected
def source_dropdown_clicked(event):
    config.selected_source = event.target.value
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
    

