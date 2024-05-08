from js import localStorage
from js import setInterval
from js import clearInterval
from js import window
from js import console, XMLHttpRequest
from pyscript import document
from pyweb import pydom
from Article import *
from pyodide.ffi import create_proxy
import config
import local_storage
import json

# list of articles selected on index.html (Article objects)
selected_articles = local_storage.retrieve_articles()
if len(selected_articles) == 0:
    local_storage.clear_local_storage()     # clear localStorage
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


# LLM Code ------------------------------------------->

# Get API Key from file
f = open("key.txt", "r")
OPENAI_API_KEY = f.read()

# LLM variables
model = "gpt-4"
llm_instructions = "You will be provided with a number of news articles. Your task is to summarize all key points mentioned in them in 5 paragraphs or less."
selected_articles_content = ""

# Iterate thru selected_articles and combine their content
for article in selected_articles:
    article.content = article.content[:250].strip().replace("\n", " ")
    selected_articles_content = selected_articles_content + article.content

messages = [
    {"role": "system", "content": llm_instructions},
    {"role": "user", "content": selected_articles_content}
]
temperature = 0.7
max_tokens = 2000
top_p = 1


# HTTP Request ---------------------------------->

xhr = XMLHttpRequest.new()
xhr.open("POST", "https://api.openai.com/v1/chat/completions", False)
xhr.setRequestHeader("Content-Type", "application/json")
xhr.setRequestHeader("Authorization", "Bearer " + OPENAI_API_KEY)

data = json.dumps({
    "model": model,
    "messages": messages,
    "temperature": temperature,
    "max_tokens": max_tokens,
    "top_p": top_p,
})

xhr.send(data)

json_response = json.loads(xhr.response)
print(json_response)
summary = json_response["choices"][0]["message"]["content"]

# -------------------------------------<
local_storage.save_articles_summary(summary)    # save summary to localStorage
clearInterval(interval_id)  # stop counter
window.location.href = "summary.html" # redirect to summary page
# ------------------------------------------------------------<

