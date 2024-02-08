#file Database.py
import sqlite3;

# Class for the database that stores all web scraper data.
class Database:

    # Constructor
    # Initializes the database
    def __init__(self):
        print("Connecting to database...\n")
        # Open connection
        # If database does not exist, create it
        self.con = sqlite3.connect("../database/scraper_data.db")
        self.cur = self.con.cursor()

        print("Database connected.\n")


        # Create table in database. Index off tag
        # Format    tag: Type String, category of article
        #           title: Type String, title of article
        #           source: Type String, name of source
        #           date: Type String, date of publication
        #           url: Type String, URL of article
        #           content: Type String, content of article
        self.cur.execute("CREATE TABLE IF NOT EXISTS articles(tag, title, source, date, url, content)")
        self.cur.execute("CREATE INDEX IF NOT EXISTS tag_idx ON articles(tag)")

    # Insert article into database
    # Ensures no duplicates
    # article of type Article
    def insert_article(self, article):
        res = self.cur.execute("SELECT * FROM articles WHERE url LIKE ?", (article.url,))  # Check for duplicates
        if res.fetchone() is None:
            self.cur.execute("""INSERT INTO articles VALUES (?, ?, ?, ?, ?, ?)""", article.get_tuple())  # insert
            self.con.commit()

    # Get articles from database by tag
    # Returns empty list if no matches
    def get_articles(self, tag):
        res = self.cur.execute("SELECT * FROM articles WHERE tag = ?", (tag,))
        return res.fetchall()

    # Prints articles with specified tag
    def print_articles(self, tag):
        res = self.cur.execute("SELECT * FROM articles WHERE tag = ?", (tag,))
        print(*(res.fetchall()), sep="\n")

    # Destructor
    # Closes connection to database
    def __del__(self):
        self.con.close()
        print("Database connection closed.")


