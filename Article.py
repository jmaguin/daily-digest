#file: Article.py

# Class to define articles collected by the scrapers
class Article:
    
    # Constructor
    # All variables are Strings
    def __init__(self, tag, title, source, date, url, content):
        self.tag = str(tag)
        self.title = str(title)
        self.source = str(source)
        self.date = str(date)
        self.url = str(url)
        self.content = str(content)

    # Returns a formatted tuple for use in SQL querys
    def get_tuple(self):
        return (self.tag, self.title, self.source, self.date, self.url, self.content)
    
    # called when article is printed
    def __str__(self):
        return_string = "[%s]\n%s - %s\n\"%s\"\n%s\n%s" % (self.tag, self.source, self.date, self.title, self.content, self.url)
        return return_string


