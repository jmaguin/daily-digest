#file ScraperDatabase.py

import sqlite3;

# Class for the database that stores all web scraper data.
class Database:

    # Constructor
    # Initializes the database
    def __init__(self):
        # Open connection
        # If database does not exist, create it
        self.con = sqlite3.connect("scraper_data.db")
        self.cur = self.con.cursor()

        # Create table in database
        # Format    source: Type String, name of source
        #           tag: Type String, category of article
        #           date: Type String, date of publication
        #           url: Type String, URL of article
        #           content: Type String, content of article
        self.cur.execute("CREATE TABLE IF NOT EXISTS articles(source, tag, date, url, content)")

    # Insert article into database
    # Ensures no duplicates
    def insert_article(self, source, tag, date, url, content):
        res = self.cur.execute("SELECT * FROM articles WHERE url LIKE ?", url)  # Check for duplicates
        if res.fetchone() is None:
            self.cur.execute("""INSERT INTO articles VALUES (?, ?, ?, ?, ?)""", (source, tag, date, url, content))  # insert
            self.con.commit()

    # Get articles from database by tag
    # Returns empty list if no matches
    def get_articles(self, tag):
        res = self.cur.execute("SELECT source, date, url, content FROM articles WHERE tag = %s ORDER BY date" % tag)
        return res.fetchall()

    # Prints articles with specified tag
    def print_articles(self, tag):
        res = self.cur.execute("SELECT source, date, url, content FROM articles WHERE tag = %s ORDER BY date" % tag)
        print(*(res.fetchall()), sep="\n")

    # Destructor
    # Closes connection to database
    def __del__(self):
        self.con.close()


