#file database.py

import sqlite3;

# Class for the database that stores all web scraper data.
class Database:

    # Constructor
    # Initializes the database
    def __init__(self):
        # Open connection
        # If database does not exist, create it
        self.con = sqlite3.connect("scraper_data.db")
        self.cur = con.cursor()

        # Create table in database
        # Format    source: Type String, name of source
        #           tags: Type List, list of relevant tags
        #           date: Type datetime, date of publication
        #           content: Type String, content of article
        self.cur.execute("CREATE TABLE IF NOT EXISTS articles(source TEXT, tags, date, content)")

    # Insert article into database
    def insert_article(source, tags, date, content):
        cur.execute("INSERT INTO articles VALUES (source, tags, date, content)")


