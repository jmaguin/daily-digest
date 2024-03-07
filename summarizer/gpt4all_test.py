import sys
import os
import time
import sqlite3

sys.path.append('../summarizer')
from gpt4all_summarizer import Summarizer

if  __name__ == "__main__":
	# os.chdir('..')
	print("Running ...\n")

    # Instantiate database
	con = sqlite3.connect("../database/scraper_data.db")
	cur = con.cursor()

	# Should return a list of tuples
	articles = cur.execute('SELECT content, title, url FROM articles WHERE tag = "politics" LIMIT 2').fetchall()

	# print(type(articles))
	# print(articles)

	# Start Timer
	start_time = time.time()

	summarizer = Summarizer()
	output = summarizer.summarizeArticles(articles)

	end_time = time.time()
	print("---------- Execution time: %ssec ----------" % round(end_time-start_time, 2))
	print("The output:\n")
	print(output)
	# Print execution time