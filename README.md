# web-scraper

## Running instructions:
1. Download project
2. run 'python main.py'  
Note: sqlite3 is included in Python. No install is necessary.

## Creating a New Scraper:
1. Create a new file and within it the scraper class
2. Extend the abstract class WebScraper.py
4. Study the HTML structure of the desired webpage
3. Implement the required methods
- look at other files as examples

## Files:
main.py  
WebScraper.py  
Database.py  
Data sources:  
- PbsNewshour.py  

### main.py
- creates new instances of all data sources
- saves collected data to sqlite3 database

### WebScraper.py
- abstract class to construct all web scrapers from
- methods:
    ```
    def __init__(self, num_of_entries)
        # num_of_entries = number of entries in the database table
        # initialization of the object
        # define tags/categories to collect data for
        # get pages for each tag/category
        # get articles from each page
        
    def get_articles(self, tag)
        # returns a List of all articles in from specified tag gathered by the scraper
        
    def get_tags(self)
        # returns a List of all of the tags/categories specified in __init__

    def print_articles(self)
        # prints all found articles in the format:
            # <Article Title>: tag1, tag2, tag3 ...
    ```
### Database.py
- sqlite3 persistent databse
- stores all data from all web scrapers
- Table entries are:
    - source:   String      name of source
    - tag:      String      relevant tag
    - date:     datetime    date of publication
    - content:  String      content of article
- methods:
    ```
    def __init__(self)
        # initializes the database (db)
        # Opens the connection to the db
        # if db does not exist, create it
        # create table in the database with above entries

    def insert_article(source, tags, date, content)
        # inserts an article with the above information into the database
    ```
    


