#file: model.py

from enum import Enum
from pathlib import Path
from os.path import abspath
import time
from gpt4all import GPT4All

print("Running ...")
start_time = round(time.time(), 1)

# model paths
mistral_path = Path("/daily-digest/models/mistral-7b-instruct-v0.1.Q4_0.gguf")
print(abspath("summarizer.py"))

# track downloaded models
class Model(Enum):
    MISTRAL = "C:/Users/jackm/Documents/School/Senior/daily-digest/models/mistral-7b-instruct-v0.1.Q4_0.gguf"
    ORCA = "C:/Users/jackm/Documents/School/Senior/daily-digest/models/orca-mini-3b-gguf2-q4_0.gguf"

text = "Former Maryland Gov. Larry Hogan announced Friday that he will run for U.S. Senate, giving Republicans a prominent candidate who is well-positioned to run a competitive campaign for the GOP in a state that hasn’t had a Republican U.S. senator in 37 years. The decision marks a surprise turnaround for Hogan, a moderate who had considered a presidential bid. During Hogan’s tenure as governor, he became a national figure as one of the rare Republicans willing to criticize Donald Trump. Last month, Hogan stepped down from the leadership of the third-party movement No Labels."
query = "Summarize the following text: " + text

model = GPT4All(Model.ORCA.value)

with model.chat_session():
    model.generate("What is the longest month?", max_tokens=40)
    output = model.current_chat_session[2]['content']

# Print output and execution time
print(output)
end_time = round(time.time(), 1)
print("---------- Execution time: %ssec ----------" % (end_time-start_time))