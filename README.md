# daily-digest

## Installation Instructions:
1. Download project
2. Install GPT4All with ```pip install gpt4all```
3. Download a GPT4All model from: https://gpt4all.io/index.html
4. Place the ".gguf" model into the /daily-digest/models/ folder.
5. Ensure the Enum in /language_model/model_enum.py is updated to reflect the downloaded model's file path.

## Scraper Running instructions:
1. Download project
2. navigate to /daily-digest/scraper. run ```python scraper_main.py``` or ```python -W ignore scraper_main.py``` to ignore warnings  
Note: sqlite3 is included in Python. No install is necessary.

## Creating a New Scraper:
1. Create a new file and within it the scraper class
2. Extend the abstract class WebScraper.py
4. Study the HTML structure of the desired webpage
3. Implement the required methods
- look at other files as examples

## Summarizer Running Instructions:
1. Download project
2. navigate to /daily-digest/language_model. run ```python summarizer.py```
Note: Ensure GPT4All is installed.

## Files:
### Scraper
Article.py  
ProgressBar.py  
WebScraper.py   
scraper_main.py     
Ap.py    
Npr.py     
PbsNewshour.py

### Database
Database.py  
scraper_data.db

### Language_Model
model_enum.py    
summarizer.py    
summarizer_main.py    

### Models
Place your .gguf models here

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

### scraper_main.py
- creates new instances of all scrapers
- creates new instance of database
- saves collected articles to sqlite3 database

### Ap.py / Npr.py / PbsNewshour.py
- scrapers that collect data
- utilize BeautifulSoup4 to parse HTML pages

### Database.py
- sqlite3 persistent databse
- stores all data from all web scrapers
- all table columns are Strings
- Table columns are:
    - tag: relevant tag
    - title: title of article
    - source: name of source
    - date: date of publication
    - url: URL of article
    - content: content of article
- table indexed based off tag

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

### scraper_data.db
- SQLite database that stores all scraped data
- can view using SQLite Studio: https://sqlitestudio.pl/

### model_enum.py    
- enum that defines the absolute path of every downloaded model
- update this file after downloading a new file to /daily-digest/models/.

### summarizer.py   
- Instantiates a new GPT4All instance using the specified model
