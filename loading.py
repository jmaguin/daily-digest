from js import localStorage
from js import setInterval
from js import clearInterval
from js import window
from pyscript import document
from pyweb import pydom
from Article import *
from pyodide.ffi import create_proxy
import config
import local_storage

# Color palette -> from index.css
gray = "#444444"
dark_gray = "#313131"
darkest_gray = "#292929"
text_color = "#c0c0c0"
accent_color = "#58a858"
dark_accent_color = "#438143"
darkest_accent_color = "#346634"

# list of articles selected on index.html (Article objects)
selected_articles = local_storage.retrieve_articles()
if len(selected_articles) == 0:
    local_storage.clear_temp_local_storage()     # clear localStorage
    window.location.href = "index.html" # redirect back to home page

timer_value = 0 # starting value for timer to count from
timer_element = document.querySelector("h2")   # select <h2>


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
summary = "Hello this is my summary and it is very cool and accurate."




# Save summary
local_storage.save_articles_summary(summary)
# ------------------------------------------------------------<

window.location.href = "summary.html" # redirect to summary page
clearInterval(interval_id)  # stop counter