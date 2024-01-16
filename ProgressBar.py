#file: ProgressBar.py

# Class to print progress bar as scraper is working
class ProgressBar:

    # Constructor
    # Initialize progress bar
    def __init__(self, page_range):
        self.cursor = 0
        self.page_range = page_range
        self.progress_bar = ["."] * (page_range + 2)
        self.progress_bar[0] = "["
        self.progress_bar[len(self.progress_bar)-1] = "]"
        print("\r%d of %d pages complete %s" % (0, self.page_range, self.prog_bar_string()), end="")

    # Converts progress_bar list to string
    def prog_bar_string(self):
        return "".join(self.progress_bar)
    
    # Prints progress of scraper
    # Call when reach next page
    def update_progress(self):
        if self.cursor < self.page_range: 
            self.cursor+=1
            self.progress_bar[self.cursor] = "="
        print("\r%d of %d pages complete %s" % (self.cursor, self.page_range, self.prog_bar_string()), end="")
    
