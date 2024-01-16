#file: Article.py

# Class to define articles collected by the scrapers
class Article:
    
    # Constructor
    # All variables are Strings
    def __init__(self, source, title, tag, date, url, content):
        self.source = str(source)
        self.title = title
        self.tag = tag
        self.date = date
        self.url = url
        self.content = content

    # Returns a formatted tuple for use in SQL querys
    def get_tuple(self):
        return (self.source, self.title, self.tag, self.date, self.url, self.content)


