from js import localStorage
from pyscript import document
from pyweb import pydom
import config
from Database import *
from Article import *
import sqlite3


# Color palette -> from index.css
gray = "#444444"
dark_gray = "#313131"
darkest_gray = "#292929"
text_color = "#c0c0c0"
accent_color = "#58a858"
dark_accent_color = "#438143"
darkest_accent_color = "#346634"

selected_topic = "politics" # value of the topic dropdown menu in index.html
selected_source = "All" # value of the source dropdown menu in index.html
selected_urls = []  # tracks all articles the user has selected. URLs (strings)
search_term = ""    # value of search bar

# Instantiate database
db = Database()

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
    new_link.innerText = article.title          # set title

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
    articles_list = db.get_articles(selected_topic)
    print(len(articles_list))
    main_element = document.querySelector("main")   # select <main>
    main_element.innerHTML = ""     # clear main
    global search_term
    
    # loop through all articles
    i = 0
    for article in articles_list:
        new_article = create_article(article)   # create article

        # pare down articles_list to just ones from specified source (source_dropdown)
        if source_dropdown.value == "All" or source_dropdown.value == article.source:

            # restrict articles based on search term (unless it's empty)
            if search_term.lower() in article.title.lower() or search_term == "":
                main_element.append(new_article)    # append article to <main>

                # re-do all styling for articles that have been selected
                for url in selected_urls:
                    if(url == article.url):
                        new_article.style.backgroundColor = darkest_gray

                i = i + 1
                if(i > 50):
                    break
    
    search_bar = document.querySelector("input")    # select search bar
    search_bar.value = ""           # clear search bar
    search_term = ""                # clear search_term

refresh_articles()

# Event Listeners ------------------------------------------

# called when generate button clicked
# enter selected article's URLs into local storage
def generate(event):
    localStorage.setItem(config.localStorage_lenth_key, str(len(selected_urls)))    # holds number of selected articles
    for i, url in enumerate(selected_urls):
        key = "url" + str(i)
        localStorage.setItem(key, url)

# called when new dropdown item selected
def topic_dropdown_clicked(event):
    global selected_topic
    selected_topic = event.target.value
    refresh_articles()

# called when new dropdown item selected
def source_dropdown_clicked(event):
    global selected_source
    selected_source = event.target.value
    refresh_articles()

# called when keydown event triggered in search bar
def search_bar_entered(event):
    global search_term
    if event.key == "Enter":
        search_term = event.target.value    # update search term
        print(search_term)
        refresh_articles()                  # update displayed articles

# called when article clicked
def article_clicked(event):
    selected_article_html = event.currentTarget     # HTML object of selected article
    selected_article_url = selected_article_html.querySelector("a").href

    # iterate thru selected_articles
    # check to see if already clicked
    for url in selected_urls:
        # article has already been clicked
        if selected_article_url == url:
            selected_urls.remove(selected_article_url)
            selected_article_html.style.backgroundColor = gray
            # update article counter
            article_count.innerHTML = "Articles Selected: " + str(len(selected_urls)) + "/" + str(config.max_selection)
            return

    # if num of selected articles lower than max allowed, select it
    if len(selected_urls) < config.max_selection:
        selected_urls.append(selected_article_url)
        selected_article_html.style.backgroundColor = darkest_gray

    # update article counter
    article_count.innerHTML = "Articles Selected: " + str(len(selected_urls)) + "/" + str(config.max_selection)
    

