from js import localStorage
from js import window
from pyscript import document
from pyweb import pydom
from pyodide.ffi import create_proxy
import json
import config
import local_storage
from Database import *
from Article import *
import sqlite3

selected_topic = "politics" # value of the topic dropdown menu in index.html
selected_source = "All" # value of the source dropdown menu in index.html
selected_urls = []  # tracks all articles the user has selected. URLs (strings)
liked_articles = [] # keeps track of liked articles
search_term = ""    # value of search bar
max_num_displayed_articles = config.display_article_increment    # total number of articles to display

# Instantiate database
db = Database()

# Populate dropdowns in the header -------------------------------------------------

# populate the topics dropdown
topic_dropdown = document.getElementById("topicDropdown")  # find dropdown element
topic_dropdown.setAttribute("py-click", "topic_dropdown_clicked")
for topic in config.master_tags:
    new_option = document.createElement("option")   # create option element
    new_option.value = topic
    new_option.innerText = topic.capitalize()
    topic_dropdown.append(new_option) # append to DOM

# populate the sources dropdown
source_dropdown = document.getElementById("sourceDropdown")  # find dropdown element
source_dropdown.setAttribute("py-click", "source_dropdown_clicked")
for art_source in config.master_sources:
    new_option = document.createElement("option")   # create option element
    new_option.value = art_source
    new_option.innerText = art_source
    source_dropdown.append(new_option) # append to DOM

# ---------------------------------------------------------------------------------

# intitialize article counter
article_count = document.querySelector(".articleCount")
article_count.innerText = "Articles Selected: 0/" + str(config.max_selection)

# Helper functions -----------------------------------------------------------------

# Set multiple attributes easily
# Input: elem = DOM element, attrs = dictionary
# Output: none
def setAttributes(elem, attrs):         
    for key, value in attrs.items():
        elem.setAttribute(key, value)

# ----------------------------------------------------------------------------------


# Event Listeners ------------------------------------------

# called when generate button clicked
# Query database to turn selected_urls into Article objects
# Save Article objects into localStorage
def generate(event):
    # if no selected articles, do nothing
    if len(selected_urls) == 0:
        return
    
    # Save selected URLs as Article objects in localStorage
    selected_articles = []
    for url in selected_urls:
        selected_articles.append(db.get_article(url))
    local_storage.save_articles(selected_articles)

    window.location.href = "loading.html" # redirect to loading page

# called when new dropdown item selected
def topic_dropdown_clicked(event):
    global selected_topic
    selected_topic = event.target.value
    refresh_articles(False)

# called when new dropdown item selected
def source_dropdown_clicked(event):
    global selected_source
    selected_source = event.target.value
    refresh_articles(False)

# called when keydown event triggered in search bar
def search_bar_entered(event):
    global search_term
    if event.key == "Enter":
        search_term = event.target.value    # update search term
        refresh_articles(True)              # update displayed articles

# called when < See More > Button clicked
def see_more_button_clicked(event):
    global max_num_displayed_articles
    max_num_displayed_articles += config.display_article_increment
    refresh_articles(True)  # True passed to keep search term

# called when < See Less > Button clicked
def see_less_button_clicked(event):
    global max_num_displayed_articles
    if(max_num_displayed_articles > config.display_article_increment):
        max_num_displayed_articles -= config.display_article_increment
        refresh_articles(True)  # True passed to keep search term

# called when article clicked
def article_clicked(event):
    selected_article_html = event.currentTarget     # HTML object of selected article
    selected_article_url = selected_article_html.querySelector("a").href

    # iterate thru selected_urls
    # check to see if already clicked
    for url in selected_urls:
        # article has already been clicked
        if selected_article_url == url:
            selected_urls.remove(selected_article_url)
            selected_article_html.style.backgroundColor = config.gray
            # update article counter
            article_count.innerHTML = "Articles Selected: " + str(len(selected_urls)) + "/" + str(config.max_selection)
            return

    # if num of selected articles lower than max allowed, select it
    if len(selected_urls) < config.max_selection:
        selected_urls.append(selected_article_url)
        selected_article_html.style.backgroundColor = config.darkest_gray

    # update article counter
    article_count.innerHTML = "Articles Selected: " + str(len(selected_urls)) + "/" + str(config.max_selection)

def article_pointer_down(event):
    selected_article_html = event.currentTarget
    # make article shrink on pointer down by adding a class
    selected_article_html.style.transition = "0.1s"
    selected_article_html.style.transform = f"scale(0.98)"

def article_pointer_up(event):
    selected_article_html = event.currentTarget
    # stop shrink by removing the class
    selected_article_html.style.transform = f"scale(1)"

def action_pointer_down(event):
    # print("STOP PROPAGATING")
    selected_button = event.currentTarget
    event.stopPropagation()

def interested_clicked(event):
    print("interested clicked")
    selected_button = event.currentTarget

    # change img color
    selected_image = selected_button.querySelector("img")
    # selected_image.src = "./assets/svg/thumbs-up-active.svg"

    selected_button.setAttribute("id", "intrested")
    liked_articles.append("hey")
    liked_articles.append("yo")

    print(json.dumps(liked_articles))

    localStorage.setItem("liked_articles", json.dumps(liked_articles))

    liked2 = localStorage.getItem("liked_articles")
    liked3 = json.loads(liked2)

    liked3.append("omg")
    print(type(liked2))
    print(liked3)

    event.stopPropagation()
    
def uninterested_clicked(event):
    print("unintereseted clicked")
    event.stopPropagation()

def bookmark_clicked(event):
    print("bookmark clicked")
    event.stopPropagation()

# --------------------------------------------------------------------

# Creates and appends elements to action_bar
# Input: none
# Output: newly setup action_bar <div>
def create_action_bar():
    # create <div> for actions bar
    new_action_bar = document.createElement("div")
    new_action_bar.classList.add("actions-bar")

    # create <ul> for left-side and right-side of actions bar
    actions_left_list = []      # holds list of elements to put into new_actions_left
    actions_right_list = []     # holds list of elements to put into new_actions_right
    
    new_actions_left = document.createElement("ul")
    new_actions_left.classList.add("actions-ul", "actions-ul-left")
    
    new_actions_right = document.createElement("ul")
    new_actions_right.classList.add("actions-ul", "actions-ul-right")

    # create <li> for left-side and right-side action buttons
    # interested button
    new_interested = document.createElement("li")
    new_interested.classList.add("action-li", "interested-li")

    new_interested_button = document.createElement("button")
    new_interested_button.classList.add("action-button", "interested-button")
    setAttributes(new_interested_button, {"type": "button", "py-click": "interested_clicked"})

    new_interested_img = document.createElement("img")
    setAttributes(new_interested_img, {"src": "./assets/svg/thumbs-up-neutral.svg", "alt": "thumbs up icon", "height": "30px", "width": "30px"})

    # uninterested button
    new_uninterested = document.createElement("li") 
    new_uninterested.classList.add("action-li", "uninterested-li")

    new_uninterested_button = document.createElement("button")
    new_uninterested_button.classList.add("action-button", "uninterested-button")
    setAttributes(new_uninterested_button, {"type": "button", "py-click": "uninterested_clicked"})

    new_uninterested_img = document.createElement("img")
    setAttributes(new_uninterested_img, {"src": "./assets/svg/thumbs-down-neutral.svg", "alt": "thumbs down icon", "height": "30px", "width": "30px"})

    # bookmark button
    new_bookmark = document.createElement("li")
    new_bookmark.classList.add("action-li", "save-li")

    new_bookmark_button = document.createElement("button")
    new_bookmark_button.classList.add("action-button")
    setAttributes(new_bookmark_button, {"type": "button", "py-click": "bookmark_clicked"})

    new_bookmark_img = document.createElement("img")
    setAttributes(new_bookmark_img, {"src": "assets/svg/bookmark-neutral.svg", "alt": "bookmark icon", "height": "30px", "width": "30px"})

    actions_left_list.append((new_interested, new_interested_button, new_interested_img))
    actions_left_list.append((new_uninterested, new_uninterested_button, new_uninterested_img))
    actions_right_list.append((new_bookmark, new_bookmark_button, new_bookmark_img))

    # append left and right <li>'s to their respectives <ul>s
    for (li, button, img) in actions_left_list:
        apd = create_proxy(action_pointer_down)
        button.addEventListener("pointerdown", apd)
        button.append(img)
        li.append(button)
        new_actions_left.append(li)

    for (li, button, img) in actions_right_list:
        button.append(img)
        button.addEventListener("pointerdown", apd)
        li.append(button)
        new_actions_right.append(li)

    new_action_bar.append(new_actions_left)
    new_action_bar.append(new_actions_right)

    return new_action_bar

# Creates an article HTML element
# Input: Article object
# Returns new article
def create_article(article):
    # create article
    new_article = document.createElement("article")     # will have main <div> and action bar <div> as children
    new_article.setAttribute("py-click", "article_clicked")

    pd = create_proxy(article_pointer_down)
    new_article.addEventListener("pointerdown", pd)

    pu = create_proxy(article_pointer_up)
    new_article.addEventListener("pointerup", pu)
    new_article.addEventListener("pointerout", pu)

    # create main content <div>
    new_main = document.createElement("div")    # will house main content (main div -> h3, a, p)
    new_main.classList.add("article-main")

    # create <h3> heading
    new_header = document.createElement("h3")

    # create <a> link
    new_link = document.createElement("a")      # create link
    new_link.href = article.url                 # set link attribute
    new_link.target = "_blank"                  # open in new tab
    new_link.innerText = article.title.strip()  # set title

    # create <ul> for tags
    new_tags = document.createElement("ul")     # create tags list
    new_tags.classList.add("tags")              # add 'tags' class
    new_tag = document.createElement("li")      # create tag for date
    new_tag.innerText = article.date
    another_tag = document.createElement("li")  # create tag for source
    another_tag.innerText = article.source


    # create paragraph
    new_text = document.createElement("p")      # create paragraph
    new_text.innerText = article.content[:250].strip() + "..."   # add text blurb (250 char limit)
    
    # create action bar
    new_action_bar = create_action_bar()
    
    new_header.append(new_link)                 # place <a> into <h3>
    new_main.append(new_header)                 # place <h3> into main content <div>
    new_tags.append(new_tag)                    # place <li> into <ul>
    new_tags.append(another_tag)                # place <li> into <ul>
    new_main.append(new_tags)                   # place <ul> into main content <div>
    new_main.append(new_text)                   # place <p> into main content <div>
    new_article.append(new_main)                # append main content <div> to <article>
    new_article.append(new_action_bar)          # place .action-bar into <article>

    return new_article

# refresh displayed articles based on topic
# keep_search_term: if True, maintain article sorting by the search term
def refresh_articles(keep_search_term):
    articles_list = db.get_articles(selected_topic)
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
                        new_article.style.backgroundColor = config.darkest_gray

                i = i + 1
                if(i > max_num_displayed_articles):
                    break
        
        # if user only wants to see selected articles
        if source_dropdown.value == "Selected":

            # re-do all styling for articles that have been selected
            for url in selected_urls:
                if(url == article.url):
                    new_article.style.backgroundColor = config.darkest_gray
                    main_element.append(new_article)    # append article to <main>
    
    if keep_search_term is False:
        search_bar = document.querySelector("input")    # select search bar
        search_bar.value = ""           # clear search bar
        search_term = ""                # clear search_term

refresh_articles(False)

