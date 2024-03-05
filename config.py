# file: config.py
# contains all global variables

# master list of all tags
master_tags = ["politics",
                "world",
                "sports",
                "entertainment",
                "business",
                "science",
                "health",
                "climate",
                "technology",
                "religion",
                "nation",
                "arts",
                "economy",
                "education",
                "race",
                "culture",
                "movies",
                "food",
                "gaming",
                "television"
                ]

# master list of all sources
master_sources = ["All", "PBS Newshour", "CNN", "NPR", "AP"]

selected_topic = "politics" # value of the topic dropdown menu in index.html
selected_source = "All" # value of the source dropdown menu in index.html
selected_articles = []  # tracks all articles the user has selected. HTML objects

max_selection = 3   # max num of articles that can be selected