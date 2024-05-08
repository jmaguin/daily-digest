# daily-digest

## Installation Instructions:
1. Download project
2. Run ```pip install python-dateutil```
3. Run ```pip install python-dotenv```
4. Run ```pip install openai```
5. Run ```pip install beautifulsoup4```
6. Run ```pip install micropip```
7. Run ```pip install toml```

## Website Running Instructions:
1. Install project
2. Modify the  ```.env``` file to contain your OpenAI API key
3. Download extension: Live Server by Ritwick Dey (https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)
4. Open ```index.html``` in a VS Code tab
5. Do Ctrl + Shift + P and click the option ```Live Server: Open With Live Server```

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
    - ```master_tags```: list of strings, master list of all tags
    - ```master_sources```: list of strings, master list of all scraper's sources
    - ```selected_topic```: string, value of the topic dropdown menu in ```index.html```
    - ```selected_source```: string, value of the source dropdown menu in ```index.html```
    - ```selected_articles```: list of HTML objects, tracks all articles the user has selected
    - ```max_selection```: int, maximum number of articles the user can select

### index.html
- HTML file for homepage of the website
- ```<body>``` split into 3 sections: ```.navbar```, ```.header```, ```<main>```
- ```.navbar```
    - unordered list
    - contains logo, Daily Digest title, and "Generate" button
    - Generate button is link to loading.html page
- ```.header```
    - unordered list, below navbar
    - contains topic and source dropdowns, "Articles Selected" counter, and search bar
- ```<main>```
    - location where articles are appended after they are retrieved from the database

### index.py
- runs automatically when ```index.html``` is loaded
- It does the following upon loading the page:
1. Populates the Topics Dropdown with topics from ```master_tags``` (from config.py)
2. Populates the Source Dropdown with sources from ```master_sources``` (from config.py)
3. Creates the Article Counter. Looks like: "Articles Selected: 0/[config.max_selection]"
4. Creates a connection to the database
5. Creates an Article object for each article in the database belonging to the current selected topic and source (from dropdowns)
6. Appends those articles to the ```<main>``` tag in ```index.html```
- methods:
    ```
    def create_article(article):
        # Input: Article object
        # Creates an article HTML element and returns it
        # Text blurb limit is 250 characters

    def refresh_articles():
        # Called on page load and when Topic or Source Dropdowns change
        # Re-queries the database for articles belonging to the currently selected parameters
        # Appends all retrieved articles to the <main> tag in index.html
        # Checks styling - if an article has been selected, it should be dark gray
            # If styling is not there, apply it
    
    def generate(event):
        # Called when the "Generate" button is clicked
    
    def topic_dropdown_clicked(event):
        # Called when a new item in the Topic Dropdown is clicked
        # Updates the value of config.selected_source
        # Calls refresh_articles()

    def article_clicked(event):
        # Called when an article is clicked
        # Iterates thru config.selected_articles
            # Checks if currently selected articles is already in list
            # If so, remove it from selected_articles and update the Article Counter
        # If the number of selected articles is less than max_selection, append the article to selected_articles
        # Update Article Counter
    ```

### loading.html
- Work in Progress
- loading page for website
- loads when the user clicks the "Generate" button on ```index.html```
- ```loading.py``` automatically runs when page loads
- once summary is complete, loads ```summary.html```

### loading.py
- Work in Progress
- runs LLM that processes data from ```config.selected_articles```

### summary.html
- Work in Progress
- displays summary generated by LLM in ```loading.py```

### summary.py
- Work in Progress
- appends summary to tag in ```summary.html```

### pyscript.toml
- contains dependencies for website
- current packages: ```sqlite3``` and ```dateutil```
- If importing file from another directory to be used in a website ".py" file:
    - must add file path here

## Scraper

### Ap.py / Npr.py / PbsNewshour.py / Cnn.py
- scrapers that collect data
- utilize BeautifulSoup4 to parse HTML pages
- scrape articles upon instantiation
- extend ```WebScraper.py``` abstract class
- must implement ```reformat_date(raw_date)```
    - convert all dates to format: MON DD, YYY

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

### scraper_main.py
- File to run the scrapers
- If created a new scraper: instantiate here
- It does the following:
1. Creates connection to the database
2. Creates new instances of all scrapers
3. If a source's tag is not the same as in ```config.master_tags```, converts it
4. Loops thru all found articles and adds them to the database using ```insert_article(article)```

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
    
    def reformat_date(self, raw_date):
        # Input: Raw date String
        # Output: Properly formatted date string
        # Publication dates from different sources are in different formats
        # This function should convert all of them to MON DD, YYYY
    ```

## Database

### Database.py
- sqlite3 persistent databse
- stores all data from all web scrapers
- all table columns are strings
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
        # make table index off tag name (called ```tag_idx```)

    def insert_article(self, article)
        # Input: Article object
        # inserts an Article object into the database
        # ensures there are no duplicates
    
    def get_articles(self, tag):
        # Input: tag string
        # Gets all matching articles from database by tag
        # Returns list of Article objects
        # Returns empty list if no matches
  
    def print_articles(self, tag):
        # Input: tag string
        # Prints articles with specified tag

    def __del__(self):
        # Destructor
        # Closes connection to database
    ```

### scraper_data.db
- SQLite database that stores all scraped data
- can view using SQLite Studio: https://sqlitestudio.pl/
- Table is called ```articles```
- Table indexed off ```tag``` column
- Column format: ```tag, title, source, date, url, content```

## Assets

### base.css     
- defines basic styling for all website pages
- 7 color variables:
    - ```--gray: #444444```
    - ```--dark-gray: #313131```
    - ```--darkest-gray: #292929```
    - ```--text-color: #c0c0c0```
    - ```--accent-color: #58a858```
    - ```--dark-accent-color: #438143```
    - ```--darkest-accent-color: #346634```
- styling for: 
    - ```.navbar```
    - ```.title```
    - ```<article>``` headers and tags

### index.css     
- specific styling for ```index.html```
- styling for:
    - ```.header```
    - ```<select>``` (dropdowns)
    - ```<input>``` (search bar)
    - ```<article>``` (makes articles flexboxes)

### loading.css    
- specific styling for ```loading.html```

### summary.css    
- specific styling for ```summary.html```
- styling for:
    - ```<article>```
    - ```.citation```
