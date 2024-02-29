from datetime import datetime as dt
from pyscript import document
from pyweb import pydom
import config

# Color palette -> from index.css
gray = "#444444"
dark_gray = "#313131"
darkest_gray = "#292929"
text_color = "#c0c0c0"
accent_color = "#58a858"
dark_accent_color = "#438143"
darkest_accent_color = "#346634"

all_articles = []   # all articles for current topic
selected_articles = []  # tracks all articles the user has selected

# populate the dropdown with topics
dropdown_element = document.getElementById("dropdown" )  # find dropdown element
for topic in config.master_tags:
    new_option = document.createElement("option")   # create option element
    new_option.value = topic
    new_option.setAttribute("py-click", "dropdown_clicked")
    new_option.innerText = topic.capitalize()
    dropdown_element.append(new_option) # append to DOM

# called when generate button clicked
def generate(event):
    print("generate!")

# called when new dropdown item selected
def dropdown_clicked(event):
    config.selected_topic = event.target.value
    print(config.selected_topic)

# called when article clicked
def article_clicked(event):
    article = event.currentTarget
    
    # if article not already clicked
    if article not in selected_articles:
        # if num of selected articles lower than max allowed
        if len(selected_articles) < config.max_selection:
            selected_articles.append(article)
            article.style.backgroundColor = darkest_gray
    # unclick article
    else:
        selected_articles.remove(article)
        article.style.backgroundColor = gray
