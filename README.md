# web-scraper

## Running instructions:
1. Download project
2. run ```python main.py``` or ```python -W ignore main.py``` to ignore warnings  
Note: sqlite3 is included in Python. No install is necessary.

## Creating a New Scraper:
1. Create a new file and within it the scraper class
2. Extend the abstract class WebScraper.py
4. Study the HTML structure of the desired webpage
3. Implement the required methods
- look at other files as examples

## Files:
Article.py  
Database.py  
main.py  
ProgressBar.py  
WebScraper.py    

Data sources:  
- PbsNewshour.py  

### Article.py
- class to define each Article collected by the scrapers
- methods:
    ```
    def __init__(self, source, title, tag, date, url, content):
        # Constructor
        # All variables are Strings
    
    def get_tuple(self):
        # Returns a formatted tuple for use in SQL querys
    ```

### Database.py
- sqlite3 persistent databse
- stores all data from all web scrapers
- Table columns are:
    - source:   String      name of source
    - title:    String      title of article
    - tag:      String      relevant tag
    - date:     String      date of publication
    - url:      String      URL of article
    - content:  String      content of article

- methods:
    ```
    def __init__(self)
        # initializes the database (db)
        # Opens the connection to the db
        # if db does not exist, create it
        # create table in the database with columns defined above

    def insert_article(self, article)
        # inserts an Article object into the database
        # ensures there are no duplicates
    
    def get_articles(self, tag):
        # Gets all matching articles from database by tag
        # Returns empty list if no matches
  
    def print_articles(self, tag):
        # Prints articles with specified tag

    def __del__(self):
        # Destructor
        # Closes connection to database
    ```

### main.py
- creates new instances of all scrapers
- creates new instance of database
- saves collected articles to sqlite3 database

### ProgressBar.py
- prints progress as scraper is working
- methods:
    ```
    def __init__(self, page_range, tag):
        # Constructor
        # page_range    int     # of pages being scraped
        # tag           String  tag being scraped
        # Initialize and print progress bar
    
    def update_progress(self):
        # Reprints progress bar
        # Call when scraper reaches next page
    ```

### WebScraper.py
- abstract class to construct all web scrapers from
- methods:
    ```
    def __init__(self)
        # initialization of the object
        # define tags/categories to collect data for
        # get pages for each tag/category
        # get articles from each page
    
    def create_article(self, tag, url):
        # tag   String  tag of article
        # url   String  url of article
        # Retrieve all information about article from its URL
        # Returns Article oject
        # Returns None if fails

    def print_articles(self)
        # prints all found articles
    ```
    


