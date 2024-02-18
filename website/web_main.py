import sys
from datetime import datetime as dt
from pyscript import document
from pyweb import pydom

articles = []

def q(selector, root=document):
    return root.querySelector(selector)

# Instantiate database
# db = Database()

# article and dropdown templates
# used to add new articles
article_template = pydom.Element(q("#article-template").content.querySelector("label"))
dropdown_template = pydom.Element(q("#dropdown-template").content.querySelector("option"))

article_list = pydom["#list-tasks-container"][0]
new_article_content = pydom["#new-task-content"][0]


def add_task(e):
    # ignore empty task
    if not new_article_content.value:
        return None

    # create task
    task_id = f"task-{len(articles)}"
    article = {
        "id": task_id,
        "content": new_article_content.value,
        "done": False,
        "created_at": dt.now(),
    }

    articles.append(article)

    # add the task element to the page as new node in the list by cloning from a
    # template
    article_html = article_template.clone()
    article_html.id = task_id

    article_html_check = article_html.find("input")[0]
    article_html_content = article_html.find("p")[0]
    article_html_content._js.textContent = article["content"]
    article_list.append(article_html)

    def check_task(evt=None):
        article["done"] = not article["done"]
        article_html_content._js.classList.toggle("line-through", article["done"])

    new_article_content.value = ""
    article_html_check._js.onclick = check_task


def add_task_event(e):
    if e.key == "Enter":
        add_task(e)


new_article_content.onkeypress = add_task_event
