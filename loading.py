from js import localStorage
from js import setInterval
from js import clearInterval
from js import window
from pyscript import document
from pyweb import pydom
from Article import *
from pyodide.ffi import create_proxy
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI
import config
import local_storage
import os

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
summary = "Error"

load_dotenv(find_dotenv())  # load API key from .env
client = OpenAI(api_key=os.getenv("API_KEY"))   # Open connection to OpenAI using API_KEY

# LLM variables
model = "gpt-4"
llm_instructions = "You will be provided with a number of news articles. Your task is to summarize all key points mentioned in them in 5 paragraphs or less."
selected_articles_content = ""

# Iterate thru selected_articles and combine their content
for article in selected_articles:
    selected_articles_content = selected_articles_content + "\n" + article.content

print(selected_articles_content)

messages = [
    {"role": "system", "content": llm_instructions},
    {"role": "user", "content": selected_articles_content}
]
temperature = 0.7
max_tokens = 1000
top_p = 1

# Generate summary
completion = client.chat.completions.create(
    model = model,
    messages = messages,
    temperature = temperature,
    max_tokens = max_tokens,
    top_p = top_p
)

summary = completion.choices[0].message.content
print(summary)

local_storage.save_articles_summary(summary)    # save summary to localStorage
# ------------------------------------------------------------<

window.location.href = "summary.html" # redirect to summary page
clearInterval(interval_id)  # stop counter