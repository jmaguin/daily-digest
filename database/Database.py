#file Database.py
import sqlite3
import sys
sys.path.append("../daily_digest/Article")
from Article import *
# import dateutil.parser
# import datetime

# Class for the database that stores all web scraper data.
class Database:

    # Constructor
    # Initializes the database
    def __init__(self):
        print("Connecting to database...")
        # Open connection
        # If database does not exist, create it
        self.con = sqlite3.connect("scraper_data.db")
        self.cur = self.con.cursor()

        print("Database connected.")

        # Create table in database. Index off tag
        # Format    tag: Type String, category of article
        #           title: Type String, title of article
        #           source: Type String, name of source
        #           date: Type String, date of publication
        #           url: Type String, URL of article
        #           content: Type String, content of article
        self.cur.execute("CREATE TABLE IF NOT EXISTS articles(tag, title, source, date, url, content)")
        self.cur.execute("CREATE INDEX IF NOT EXISTS tag_idx ON articles(tag)")

    def get_con(self):
        return self.con
    
    # Insert article into database
    # Ensures no duplicates
    # article of type Article
    def insert_article(self, article):
        res = self.cur.execute("SELECT * FROM articles WHERE url LIKE ?", (article.url,))  # Check for duplicates
        if res.fetchone() is None:
            self.cur.execute("""INSERT INTO articles VALUES (?, ?, ?, ?, ?, ?)""", article.get_tuple())  # insert
            self.con.commit()

    # Get articles from database by tag
    # Returns list of Article objects
    # Returns empty list if no matches
    def get_articles(self, tag):
        res = self.cur.execute("SELECT * FROM articles WHERE tag='%s'" % tag)
            
        tup_list = res.fetchall()   # list of article tuples
        art_list = []   # list of article objects
        for tup in tup_list:
            this_article = Article(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
            art_list.append(this_article)
        return art_list

    def get_all_articles(self):
        res = self.cur.execute("SELECT * FROM articles")
        
        tup_list = res.fetchall()   # list of article tuples
        art_list = []   # list of article objects
        for tup in tup_list:
            this_article = Article(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
            art_list.append(this_article)
        return art_list

    # Get single article from database by URL
    # Returns Article object
    # Returns None if no matches
    def get_article(self, url):
        res = self.cur.execute("SELECT * FROM articles WHERE url='%s'" % url)
        tup = res.fetchone()   # tuple of strings
        if tup is None:
            return None
        
        return Article(tup[0], tup[1], tup[2], tup[3], tup[4], tup[5])
           

    # Prints articles with specified tag
    def print_articles(self, tag):
        art_list = get_articles(tag)
        for art in art_list:
            print(art)

    # Destructor
    # Closes connection to database
    def __del__(self):
        self.con.close()
        print("Database connection closed.")
