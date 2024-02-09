#file: summarizer.py

import time
import sys
from gpt4all import GPT4All
from model_enum import Model
sys.path.insert(1, "../database")
from Database import Database

print("Running ...")
start_time = time.time()

model = GPT4All(str(Model.MISTRAL.value))  # create model

with model.chat_session():
    model.generate("What is the longest month?", max_tokens=40)
    output = model.current_chat_session[2]['content']

# Print output and execution time
print(output)
end_time = time.time()
print("---------- Execution time: %ssec ----------" % round(end_time-start_time, 2))