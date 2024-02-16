#file: summarizer.py

import time
import sys
sys.path.insert(1, "../database")
from Database import Database

print("Running ...")
start_time = time.time()

# Open AI Chat GPT code here

# Print execution time
end_time = time.time()
print("---------- Execution time: %ssec ----------" % round(end_time-start_time, 2))