from js import localStorage
from js import setInterval
from js import clearInterval
from pyscript import document
from pyweb import pydom
from Database import *
from Article import *
from pyodide.ffi import create_proxy
import config



# Color palette -> from index.css
gray = "#444444"
dark_gray = "#313131"
darkest_gray = "#292929"
text_color = "#c0c0c0"
accent_color = "#58a858"
dark_accent_color = "#438143"
darkest_accent_color = "#346634"

selected_articles = []  # list of articles selected on index.html (Article objects)

timer_value = 0 # starting value for timer to count from
timer_element = document.querySelector("h2")   # select <h2>

# Begin connection to database
db = Database()

# get all selected articles using URLs from localStorage
num_of_urls = localStorage.getItem(config.localStorage_lenth_key)

# if num_of_urls is not in local storage do not try to get the urls
# this check is needed to prevent an error message from showing up
if num_of_urls is None:
    print("localStorage_length_key not found.")
    localStorage.clear()    # clear the localStorage
    # TODO: automatic redirect to previous page (index.py)?
else:
    # loop and add Article objects to selected_articles
    for i in range(int(num_of_urls)):
        url = localStorage.getItem("url" + str(i))  # retrieve url from localStorage
        this_article = db.get_article(url)  # turn URL into Article object

        # ensure article was found
        if this_article is None:
            print("Article could not be located in database.\nURL: " + url)
        else:
            selected_articles.append(this_article)

localStorage.clear()    # clear the localStorage

# Timer ---------------------------------------
# refresh timer
def update_timer():
    global timer_value
    timer_value += 1    # increment timer

    # if running for over a minute
    if timer_value >= 60:
        minutes = timer_value // 60 # // for int result
        seconds = timer_value % 60
        timer_element.innerText = str(minutes) + "min " + str(seconds) + "sec"
    else:
        timer_element.innerText = str(timer_value) + "sec"
    

# Use pyodide to create proxy for update_timer function
# Necessary to work with setInterval (javascript function)
timer_proxy = create_proxy(update_timer)
interval_id = setInterval(timer_proxy, 1000)  # call update_timer() every 1sec

# ----------------------------------------------------


# LLM Code here ------------------------------------------->



# ------------------------------------------------------------<

# Uncomment once LLM Code done
# clearInterval(interval_id)