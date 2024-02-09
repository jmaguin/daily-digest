#file: model.py

from enum import Enum
from pathlib import Path
from os.path import abspath
import time
from gpt4all import GPT4All

print("Running ...")
start_time = time.time()

# track downloaded models
class Model(Enum):
    MISTRAL = abspath("../models/mistral-7b-instruct-v0.1.Q4_0.gguf").replace('\\','/')
    ORCA = abspath("../models/orca-mini-3b-gguf2-q4_0.gguf").replace('\\','/')

model = GPT4All(str(Model.MISTRAL.value))  # create model

with model.chat_session():
    model.generate("What is the longest month?", max_tokens=40)
    output = model.current_chat_session[2]['content']

# Print output and execution time
print(output)
end_time = time.time()
print("---------- Execution time: %ssec ----------" % round(end_time-start_time, 2))