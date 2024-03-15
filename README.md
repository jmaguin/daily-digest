# daily-digest

## Installation Instructions:
1. Download project
2. Run ```pip install python-dateutil```
3. Run ```pip install openai```
4. Run ```pip install beautifulsoup4```
5. Run ```pip install micropip```
6. Run ```pip install toml```

## Scraper Running instructions:
1. Install project
2. navigate to /daily-digest. run ```python -m scraper.scraper_main.```
Note: sqlite3 is included in Python. No install is necessary.    

## Creating a New Scraper:
1. Create a new file and within it the scraper class
2. Extend the abstract class WebScraper.py
4. Study the HTML structure of the desired webpage
3. Implement the required methods
- look at other files as examples
5. Instantiate the scraper in /scraper/scraper_main.py
- create new instance e.g. ```cnn = Cnn()```
- loop through each found article and add it to the database
- ensure each tag in list of master_tags in config.py

## Website Running Instructions:
1. Install project
2. Download extension: Live Server by Ritwick Dey (https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
3. Open index.html in a VS Code tab
4. Do Ctrl + Shift + P and click the option ```Live Server: Open With Live Server```

## Files:
### Daily Digest
Article.py    
config.py    
index.html    
index.py    
loading.html     
loading.py    
summary.html    
summary.py     
pyscript.toml     

### Scraper
Ap.py     
Cnn.py    
Npr.py  
PbsNewshour.py    
ProgressBar.py  
scraper_main.py     
WebScraper.py   

### Database
Database.py  
scraper_data.db

### Assets
base.css     
index.css     
loading.css      
summary.css    

## Daily Digest

### Article.py
- class to define each Article collected by the scrapers
- Ex: accessing a field - ```article.source``` or ```article.url```
- the database stores all articles in tuple format
- use "get_tuple()" before inserting article into database
- methods:
    ```
    def __init__(self, source, title, tag, date, url, content):
        # Constructor
        # order of parameters important
        # All variables are strings
    
    def get_tuple(self):
        # Returns a formatted tuple for use in SQL querys
        # Tuple contents are in same order as constructor parameters
    ```

### config.py
- stores all global variables for Daily Digest
- variables:
    - master_tags       list of strings         master list of all tags
    - master_sources    list of strings         master list of all scraper's sources
    - selected_topic    string                  value of the topic dropdown menu in index.html
    - selected_source   string                  value of the source dropdown menu in index.html
    - selected_articles list of HTML objects    tracks all articles the user has selected
    - max_selection     int                     maximum number of articles the user can select

### index.html
- HTML file for homepage of the website
- <body> split into 3 sections: .navbar, .header, <main>
- .navbar
    - unordered list
    - contains logo, Daily Digest title, and "Generate" button
    - Generate button is link to loading.html page
- .header
    - unordered list, below navbar
    - contains topic and source dropdowns, "Articles Selected" counter, and search bar
- <main>
    - location where articles are appended after they are retrieved from the database




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
