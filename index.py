from js import localStorage
from js import window
from pyscript import document
from pyweb import pydom
from pyodide.ffi import create_proxy
import json
import config
import buttons
import local_storage
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
liked_articles = [] # keeps track of liked articles
disliked_articles = [] # keeps track of disliked articles
bookmarked_articles = [] # keeps track of bookmarked articles

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

# Shrinks article a bit on pointer down
def article_pointer_down(event):
    selected_article_html = event.currentTarget
    # make article shrink on pointer down by adding a class
    selected_article_html.style.transition = "0.1s"
    selected_article_html.style.transform = f"scale(0.98)"

# Grows article back to normal on pointer up
def article_pointer_up(event):
    selected_article_html = event.currentTarget
    # stop shrink by removing the class
    selected_article_html.style.transform = f"scale(1)"

# stops propagation on pointer down for action buttons - might not be needed anymore?
def action_pointer_down(event):
    # print("STOP PROPAGATING")
    selected_button = event.currentTarget
    event.stopPropagation()

def like_clicked(event):
    print("liked clicked")
    global liked_articles, disliked_articles

    selected_button = event.currentTarget                                                               # selected button
    selected_img = selected_button.querySelector("img")                                                 # selected img
    selected_article = selected_button.parentElement.parentElement.parentElement.parentElement          # article element of liked article
    selected_url = selected_article.querySelector("h3 a").getAttribute("href")                          # url string from href
    dislike_button = selected_button.parentElement.parentElement.querySelector(".dislike-button")       # corresponding dislike button
    dislike_img = dislike_button.querySelector("img")                                                   # img of corresponding dislike button
    
    # Toggle the button visuals and update localStorage
    buttons.toggle_like(liked_articles, disliked_articles, selected_url, selected_button, selected_img, dislike_button, dislike_img)

    # Stop Propagation in all cases
    event.stopPropagation()

    
def dislike_clicked(event):
    print("disliked clicked")
    global disliked_articles, liked_articles

    selected_button = event.currentTarget                                                       # selected button
    selected_img = selected_button.querySelector("img")                                         # selected img
    selected_article = selected_button.parentElement.parentElement.parentElement.parentElement  # article element of disliked article
    selected_url = selected_article.querySelector("h3 a").getAttribute("href")                  # url string from href
    like_button = selected_button.parentElement.parentElement.querySelector(".like-button")     # corresponding like button 
    like_img = like_button.querySelector("img")                                                 # img of corresponding like button

    # Toggle the button visuals and update localStorage
    buttons.toggle_dislike(disliked_articles, liked_articles, selected_url, selected_button, selected_img, like_button, like_img)

    # Stop Propagation in all cases
    event.stopPropagation()

def bookmark_clicked(event):
    print("bookmark clicked")
    global bookmarked_articles   # use global list variable bookmarked_articles

    selected_button = event.currentTarget                                                       # selected button
    selected_img = selected_button.querySelector("img")                                         # selected img
    selected_article = selected_button.parentElement.parentElement.parentElement.parentElement  # article element of disliked article
    selected_url = selected_article.querySelector("h3 a").getAttribute("href")                  # url string from href

    # Toggle the button visuals and update localStorage
    buttons.toggle_bookmark(bookmarked_articles, selected_url, selected_button, selected_img)
    
    # Stop Propagation in all cases
    event.stopPropagation()

# --------------------------------------------------------------------

# Creates and appends elements to action_bar
# Input: none
# Output: newly setup action_bar <div>
def create_action_bar(url):
    global liked_articles, disliked_articles, bookmarked_articles

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

    # like button
    new_like = document.createElement("li")
    new_like.classList.add("action-li", "like-li")

    new_like_button = document.createElement("button")
    new_like_button.classList.add("action-button", "like-button")
    setAttributes(new_like_button, {"type": "button", "py-click": "like_clicked"})

    new_like_img = document.createElement("img")
    like_img_src = "./assets/svg/thumbs-up-neutral.svg"
    for link in liked_articles:
        if link == url:
            like_img_src = "./assets/svg/thumbs-up-active.svg"
            break
    setAttributes(new_like_img, {"src": like_img_src, "alt": "thumbs up icon", "height": "30px", "width": "30px"})

    # dislike button
    new_dislike = document.createElement("li") 
    new_dislike.classList.add("action-li", "dislike-li")

    new_dislike_button = document.createElement("button")
    new_dislike_button.classList.add("action-button", "dislike-button")
    setAttributes(new_dislike_button, {"type": "button", "py-click": "dislike_clicked"})

    new_dislike_img = document.createElement("img")
    dislike_img_src = "./assets/svg/thumbs-down-neutral.svg"
    for link in disliked_articles:
        if link == url:
            dislike_img_src = "./assets/svg/thumbs-down-active.svg"
            break
    setAttributes(new_dislike_img, {"src": dislike_img_src, "alt": "thumbs down icon", "height": "30px", "width": "30px"})

    # bookmark button
    new_bookmark = document.createElement("li")
    new_bookmark.classList.add("action-li", "save-li")

    new_bookmark_button = document.createElement("button")
    new_bookmark_button.classList.add("action-button")
    setAttributes(new_bookmark_button, {"type": "button", "py-click": "bookmark_clicked"})

    new_bookmark_img = document.createElement("img")
    bookmark_img_src = "./assets/svg/bookmark-neutral.svg"
    for link in bookmarked_articles:
        if link == url:
            bookmark_img_src = "./assets/svg/bookmark-active.svg"
            break
    setAttributes(new_bookmark_img, {"src": bookmark_img_src, "alt": "bookmark icon", "height": "30px", "width": "30px"})

    actions_left_list.append((new_like, new_like_button, new_like_img))
    actions_left_list.append((new_dislike, new_dislike_button, new_dislike_img))
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
    new_action_bar = create_action_bar(article.url)
    
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
    print("refresh articles called")
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
                        new_article.style.backgroundColor = darkest_gray

                i = i + 1
                if(i > max_num_displayed_articles):
                    break
        
        # if user only wants to see selected articles
        if source_dropdown.value == "Selected":

            # re-do all styling for articles that have been selected
            for url in selected_urls:
                if(url == article.url):
                    new_article.style.backgroundColor = darkest_gray
                    main_element.append(new_article)    # append article to <main>
    
    if keep_search_term is False:
        search_bar = document.querySelector("input")    # select search bar
        search_bar.value = ""           # clear search bar
        search_term = ""                # clear search_term

# Update user information from Local storage
def load_user_info():
    global liked_articles, disliked_articles, bookmarked_articles
    liked_articles = local_storage.get_liked_articles()
    disliked_articles = local_storage.get_disliked_articles()
    bookmarked_articles = local_storage.get_bookmarked_articles()
    

load_user_info()
refresh_articles(False)

