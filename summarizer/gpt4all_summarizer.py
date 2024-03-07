#file: gpt4all_summarizer.py

# GPT4ALL Summarizer Class:

import sys
from pathlib import Path
from gpt4all import GPT4All


class Summarizer:

    # Constructor
    # Initializes GPT4ALL model
    def __init__(self, **kwargs):
        self.model_name = kwargs.get("model_name", 'orca-mini-3b-gguf2-q4_0.gguf')    # name of model
        self.model_path = Path(__file__).resolve().parents[0].absolute() / 'models'  # directory model is in
        
        # The following variables define values for optional arguments for GPT4All functions
        self.allow_download = kwargs.get("allow_download", False) # if true, then model initialization may download the model to model_oath
        self.max_tokens = kwargs.get("max_tokens", 200) # if "defaultMaxTokens" is passed in then use that value, if not, set it to 100
        self.temp = kwargs.get("temp", 0.8) # Larger temps increase creativity, but lower factuality 

        print(f"Initializing model: {self.model_name} in {self.model_path}\n")
        self.model = GPT4All(model_name= self.model_name, model_path= self.model_path, allow_download=self.allow_download)  # create model
    
    # summarizes articles inputed
    # Input: articles is a list of tuples (content, title, url). Optional: max_tokens and temp used in model.generate
    # Don't pass in more than a couple of articles
    # Output: Summary of passed in articles
    def summarizeArticles(self, articles, **kwargs):
        max_tokens = kwargs.get("max_tokens", self.max_tokens)
        temp = kwargs.get("temp", self.temp)
        system_template = "You summarize news articles. Try to avoid plagiaristic behavior like simplistic rewording of long passages. Try to keep direct quotations short. Try to cite your source. Do not censor yourself. There is no topic which cannot be broached. No misinformation is in these articles."

        if not isinstance(articles, list):
            print(f"Error: articles is not a list. It is a {type(articles)}")
            return

        inputString = "You summarize news articles. Try to avoid plagiaristic behavior like simplistic rewording of long passages. Try to keep direct quotations short. Try to cite your source. Do not censor yourself. There is no topic which cannot be broached. No misinformation is in these articles. \nSummarize the following news articles:\n"
        for (content, title, url) in articles:
            # if content is not str or title is not str or url is not str:
            #     print("Error: A tuple in articles is not a tuple of strings")
            #     continue
            # print(title)

            # Pass in article title and first 2000 characters of the article content
            inputString = inputString + "Title: " + title + "\nContent: " + content[:2000]
        
        print("Input String:\n" + inputString + "\n\n")
        
        testInput = "Summarize the following news, do not censor yourself: $50 Infrastructure Bill Passes House and Senate. Pokemon GO increases in popularity."
        
        with self.model.chat_session(system_template):
            response = self.model.generate(inputString, 
                                max_tokens = max_tokens, 
                                temp = temp)
            # output = self.model.current_chat_session[2]['content']
            # print(response)

            return response


