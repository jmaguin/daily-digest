# from js import localStorage
# from pyweb import pydom
from pyscript import document
from pyodide.ffi import create_proxy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import pandas as pd
import dateutil.parser as dateparser



from Database import *
from Article import *
import local_storage


# This file contains functions relating to action buttons

liked_articles = [] # keeps track of liked articles
disliked_articles = [] # keeps track of disliked articles
bookmarked_articles = [] # keeps track of bookmarked articles

update_for_you_signal = False   # signal checked in index.py to see if new likes have been added -> need to recalculate forYou list

firstTime = True

aData = None    # article data
tfidf = None
tfidf_matrix = None
cosine_sim = None
indices = None


# Helper functions -----------------------------------------------------------------

# Set multiple attributes easily
# Input: elem = DOM element, attrs = dictionary
# Output: none
def setAttributes(elem, attrs):         
    for key, value in attrs.items():
        elem.setAttribute(key, value)

# ----------------------------------------------------------------------------------

def like_clicked(event):
    # print("liked clicked")
    global update_for_you_signal

    selected_button = event.currentTarget                                                               # selected button
    selected_img = selected_button.querySelector("img")                                                 # selected img
    selected_article = selected_button.parentElement.parentElement.parentElement.parentElement          # article element of liked article
    selected_url = selected_article.querySelector("h3 a").getAttribute("href")                          # url string from href
    dislike_button = selected_button.parentElement.parentElement.querySelector(".dislike-button")       # corresponding dislike button
    dislike_img = dislike_button.querySelector("img")                                                   # img of corresponding dislike button
    
    selected_img.style.transition = "2s"
    selected_img.style.transform = f"scale(0.50)"
    selected_img.style.transform = f"scale(1)"
    # Toggle the button visuals and update localStorage
    toggle_like(selected_url, selected_button, selected_img, dislike_button, dislike_img)

    update_for_you_signal = True
    # Stop Propagation in all cases
    event.stopPropagation()

    
def dislike_clicked(event):
    # print("disliked clicked")
    global disliked_articles
    selected_button = event.currentTarget                                                       # selected button
    selected_img = selected_button.querySelector("img")                                         # selected img
    selected_article = selected_button.parentElement.parentElement.parentElement.parentElement  # article element of disliked article
    selected_url = selected_article.querySelector("h3 a").getAttribute("href")                  # url string from href
    like_button = selected_button.parentElement.parentElement.querySelector(".like-button")     # corresponding like button 
    like_img = like_button.querySelector("img")                                                 # img of corresponding like button

    # Toggle the button visuals and update localStorage
    toggle_dislike(selected_url, selected_button, selected_img, like_button, like_img)

    # print(disliked_articles)

    # Stop Propagation in all cases
    event.stopPropagation()

def bookmark_clicked(event):
    # print("bookmark clicked")
    global bookmarked_articles   # use global list variable bookmarked_articles

    selected_button = event.currentTarget                                                       # selected button
    selected_img = selected_button.querySelector("img")                                         # selected img
    selected_article = selected_button.parentElement.parentElement.parentElement.parentElement  # article element of disliked article
    selected_url = selected_article.querySelector("h3 a").getAttribute("href")                  # url string from href

    # Toggle the button visuals and update localStorage
    toggle_bookmark(bookmarked_articles, selected_url, selected_button, selected_img)
    
    # Stop Propagation in all cases
    event.stopPropagation()


# Shrinks the button a bit when pressed. Needed to stop propagation
def action_pointer_down(event):
    # print("STOP PROPAGATING")
    # selected_button = event.currentTarget
    # selected_img = selected_button.querySelector("img")
    # selected_img.style.transition = "0.05s"
    # selected_img.style.transform = f"scale(0.98)"
    event.stopPropagation()

# stops propagation on pointer down for action buttons - might not be needed anymore?
def action_pointer_up(event):
    # print("STOP PROPAGATING")
    # selected_button = event.currentTarget
    # selected_img = selected_button.querySelector("img")
    # selected_img.style.transform = f"scale(1)"
    event.stopPropagation()




# Creates and appends elements to action_bar
# Input: none
# Output: newly setup action_bar <div>
def create_action_bar(url): 
    global liked_articles, disliked_articles, bookmarked_articles
    # create <div> for actions bar
    new_action_bar = document.createElement("div")
    new_action_bar.classList.add("actions-bar")

    # create <ul> for left-side and right-side of actions bar
    actions_left_list = []      # holds list of elements to put into new_actions_left
    actions_right_list = []     # holds list of elements to put into new_actions_right
    
    new_actions_left = document.createElement("ul")
    new_actions_left.classList.add("actions-ul", "actions-ul-left")
    
    new_actions_right = document.createElement("ul")
    new_actions_right.classList.add("actions-ul", "actions-ul-right")

    # create <li> for left-side and right-side action buttons

    # like button
    new_like = document.createElement("li")
    new_like.classList.add("action-li", "like-li")

    new_like_button = document.createElement("button")
    new_like_button.classList.add("action-button", "like-button")
    setAttributes(new_like_button, {"type": "button", "py-click": "buttons.like_clicked"})

    new_like_img = document.createElement("img")
    like_img_src = "./assets/svg/thumbs-up-neutral.svg"
    for link in liked_articles:
        if link == url:
            like_img_src = "./assets/svg/thumbs-up-active.svg"
            break
    setAttributes(new_like_img, {"src": like_img_src, "alt": "thumbs up icon", "height": "30px", "width": "30px"})

    # dislike button
    new_dislike = document.createElement("li") 
    new_dislike.classList.add("action-li", "dislike-li")

    new_dislike_button = document.createElement("button")
    new_dislike_button.classList.add("action-button", "dislike-button")
    setAttributes(new_dislike_button, {"type": "button", "py-click": "buttons.dislike_clicked"})

    new_dislike_img = document.createElement("img")
    dislike_img_src = "./assets/svg/thumbs-down-neutral.svg"
    for link in disliked_articles:
        if link == url:
            dislike_img_src = "./assets/svg/thumbs-down-active.svg"
            break
    setAttributes(new_dislike_img, {"src": dislike_img_src, "alt": "thumbs down icon", "height": "30px", "width": "30px"})

    # bookmark button
    new_bookmark = document.createElement("li")
    new_bookmark.classList.add("action-li", "save-li")

    new_bookmark_button = document.createElement("button")
    new_bookmark_button.classList.add("action-button")
    setAttributes(new_bookmark_button, {"type": "button", "py-click": "buttons.bookmark_clicked"})

    new_bookmark_img = document.createElement("img")
    bookmark_img_src = "./assets/svg/bookmark-neutral.svg"
    for link in bookmarked_articles:
        if link == url:
            bookmark_img_src = "./assets/svg/bookmark-active.svg"
            break
    setAttributes(new_bookmark_img, {"src": bookmark_img_src, "alt": "bookmark icon", "height": "30px", "width": "30px"})

    actions_left_list.append((new_like, new_like_button, new_like_img))
    actions_left_list.append((new_dislike, new_dislike_button, new_dislike_img))
    actions_right_list.append((new_bookmark, new_bookmark_button, new_bookmark_img))

    apd = create_proxy(action_pointer_down)
    apu = create_proxy(action_pointer_up)

    # append left and right <li>'s to their respectives <ul>s
    for (li, button, img) in actions_left_list:
        button.addEventListener("pointerdown", apd)
        button.addEventListener("pointerup", apu)
        button.append(img)
        li.append(button)
        new_actions_left.append(li)

    for (li, button, img) in actions_right_list:
        button.addEventListener("pointerdown", apd)
        button.addEventListener("pointerup", apu)
        button.append(img)
        li.append(button)
        new_actions_right.append(li)

    new_action_bar.append(new_actions_left)
    new_action_bar.append(new_actions_right)

    return new_action_bar

# Toggle the like button (and possibly the dislike button) visuals and update localStorage
# Input: liked list, disliked list, URL string, like <button>, like <img>, dislike <button>, dislike <image>
def toggle_like(selected_url, selected_button, selected_img, dislike_button, dislike_img):
    global liked_articles, disliked_articles
    already_liked = False
    already_disliked = False

    # if no url string is found -> return
    if len(selected_url) == 0:
        return
    
    # check if url is already in liked_articles
    for url in liked_articles:
        if url == selected_url:
            already_liked = True
            break
    
    # check if url is already in disliked_articles
    for url in disliked_articles:
        if url == selected_url:
            already_disliked = True
            break
    
    # If already disliked and not already liked -> remove dislike
    if already_disliked and not already_liked:
        print("already disliked")
        dislike_button.classList.remove("disliked")                     # remove class "disliked" from button
        dislike_img.src = "./assets/svg/thumbs-down-neutral.svg"        # change img color
        disliked_articles.remove(selected_url)                          # update global disliked_articles
        local_storage.set_disliked_articles(disliked_articles)          # update localStorage

    # If already liked -> Unlike
    if already_liked == True:
        selected_button.classList.remove("liked")                       # remove class "liked" from button
        selected_img.src = "./assets/svg/thumbs-up-neutral.svg"         # change img color
        liked_articles.remove(selected_url)                             # update global liked_articles
        local_storage.set_liked_articles(liked_articles)                # update localStorage

    # If not already liked -> Like
    if not already_liked:
        selected_button.classList.add("liked")                          # add class "liked" from button
        selected_img.src = "./assets/svg/thumbs-up-active.svg"          # change img color
        liked_articles.append(selected_url)                             # update global liked_articles
        local_storage.set_liked_articles(liked_articles)                # update localStorage


# Toggle the dislike button (and possibly the like button) visuals and update localStorage
# Input: disliked list, liked list, URL string, dislike <button>, dislike <img>, like <button>, like <image>
def toggle_dislike(selected_url, selected_button, selected_img, like_button, like_img):
    global liked_articles, disliked_articles
    already_disliked = False
    already_liked = False

    # if no url string is found -> return
    if len(selected_url) == 0:
        return

    # check if url is already in disliked_articles
    for url in disliked_articles:
        if url == selected_url:
            already_disliked = True
            break

    # check if url is already in liked_articles
    for url in liked_articles:
        if url == selected_url:
            already_liked = True
            break
    
    # If already liked and not already disliked -> remove like
    if already_liked and not already_disliked:
        like_button.classList.remove("liked")                           # remove class "disliked" from button
        like_img.src = "./assets/svg/thumbs-up-neutral.svg"             # change img color
        liked_articles.remove(selected_url)                             # update global disliked_articles
        local_storage.set_liked_articles(disliked_articles)             # update localStorage

    # If already disliked -> Undislike
    if already_disliked == True:
        selected_button.classList.remove("disliked")                    # remove class "disliked" from button
        selected_img.src = "./assets/svg/thumbs-down-neutral.svg"        # change img color
        disliked_articles.remove(selected_url)                          # update global disliked_articles
        local_storage.set_disliked_articles(disliked_articles)          # update localStorage

    # If not already disliked -> dislike
    if not already_disliked:
        selected_button.classList.add("disliked")                       # add class "disliked" from button
        selected_img.src = "./assets/svg/thumbs-down-active.svg"        # change img color
        disliked_articles.append(selected_url)                          # update global disliked_articles
        local_storage.set_disliked_articles(disliked_articles)          # update localStorage


# Toggle the bookmark button visuals and update localStorage
# Input: bookmarked list, URL string, dislike <button>, dislike <img>, like <button>, like <image>
def toggle_bookmark(bookmarked_articles, selected_url, selected_button, selected_img):
    already_bookmarked = False
    # if no url string is found -> return
    if len(selected_url) == 0:
        return

    # check if url is already in bookmarked_articles
    for url in bookmarked_articles:
        if url == selected_url:
            already_bookmarked = True
            break

    # If already bookmarked -> unbookmark
    if already_bookmarked == True:
        selected_button.classList.remove("bookmarked")                  # remove class "bookmarked" from button
        selected_img.src = "./assets/svg/bookmark-neutral.svg"          # change img color
        bookmarked_articles.remove(selected_url)                        # update global bookmarked_articles
        local_storage.set_bookmarked_articles(bookmarked_articles)      # update localStorage

    # If not already bookmarked -> bookmark
    if not already_bookmarked:
        selected_button.classList.add("bookmarked")                     # add class "bookmarked" from button
        selected_img.src = "./assets/svg/bookmark-active.svg"           # change img color
        bookmarked_articles.append(selected_url)                        # update global bookmarked_articles
        local_storage.set_bookmarked_articles(bookmarked_articles)      # update localStorage

# Update user information from Local storage
def load_user_info():
    global liked_articles, disliked_articles, bookmarked_articles
    liked_articles = local_storage.get_liked_articles()
    disliked_articles = local_storage.get_disliked_articles()
    bookmarked_articles = local_storage.get_bookmarked_articles()

def initialize_data_and_matrices(db):
    print("init data")
    global liked_articles, disliked_articles, update_for_you_signal, aData, tfidf, tfidf_matrix, cosine_sim, indices
    # Load database into pandas frame
    con = db.get_con()

    if firstTime == True:
        aData = pd.read_sql_query("SELECT * from articles", con) # remember: "title", "url", "content", "date"

        # Create TfidVectorizer object to transform data into a Tf-idf representation
        
        tfidf = TfidfVectorizer(stop_words="english", max_features=20)

        # Combine title and content into a single string
        aData["titlecontent"] = aData["content"].astype(str) + " " + aData["title"].astype(str)
        aData["titlecontent"] = aData["titlecontent"].fillna("")
        tfidf_matrix = tfidf.fit_transform(aData["titlecontent"])

        # Calculate the cosine similarity matrix between articles only the first time
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        # print(type(cosine_sim))
        
        # Get indicies of aData based on url
        indices = pd.Series(aData.index, index=aData["url"]).drop_duplicates()

def getRecommendedArticles(db):
    print("Loading For You")
    global firstTime
    final_list_of_articles = []
    count = 10
    list_of_list_of_articles = []   # a list of lists of articles

    if firstTime == True:
        initialize_data_and_matrices(db)
        firstTime = False

    # get list of similar articles for every article in liked
    for url in liked_articles:
        list_of_list_of_articles.append(getSimilarArticles(url, count))
    
    if len(list_of_list_of_articles) == 0:
        return []
    
    # extend lists together
    final_list_of_articles.extend(list_of_list_of_articles[0])
    for i in range(1, len(list_of_list_of_articles)):
        list = list_of_list_of_articles[i]

        for i in range(0, len(list)):
            candidate = list[i]
            found = False

            # loop through final list, don't add duplicates
            for item in final_list_of_articles:
                if(item == candidate):
                    found = True

            if not found:
                final_list_of_articles.append(candidate)
                # print(candidate.title)
                # print(final_list_of_articles)
            else:
                print("duplicate")
            
    # sort final list of articles
    final_list_of_articles.sort(key=lambda x: dateparser.parse(x.date), reverse=True)

    update_for_you_signal = False

    return final_list_of_articles

# gets 10 similar articles specified by url
def getSimilarArticles(url, count):
    global aData, cosine_sim, indices
    # sample title and url
    # title = "New York governor wants to spend $2.4 billion to help deal with migrant influx in new budget proposal"
    # url = "https://www.pbs.org/newshour/politics/new-york-governor-wants-to-spend-2-4-billion-to-help-deal-with-migrant-influx-in-new-budget-proposal"
    
    # index of url
    index = indices[url]

    # enumerate to get (index, score) of article specified by url
    sim_scores = enumerate(cosine_sim[index])

    # sort sim_scores using lambda function (take x, sort based on x[1] (the score)) reverse=True means highest score at the top
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # # the number 1 spot will be the article itself, so get spots 2-count+1
    # sim_scores = sim_scores[1:(count+1)]
    
    # # get list of indexes from sim_scores
    # # entry looks like this: (index, score) so i[0] is index
    # sim_index = [i[0] for i in sim_scores]

    article_tuple_list = []
    added = 0
    for i, score in sim_scores:
        # print(aData["title"][i])
        if added >= count:
            break
        # don't add the liked article itself
        elif aData["url"][i] != url:
            article = Article(aData["tag"][i], aData["title"][i], aData["source"][i], aData["date"][i], aData["url"][i], aData["content"][i])
            article_tuple_list.append(article)
            added += 1
    
    return article_tuple_list

def get_bookmarked_articles(db):
    global bookmarked_articles
    print("get_bookmarked_articles")
    articles = []
    if len(bookmarked_articles) == 0:
        bookmarked_articles = local_storage.get_bookmarked_articles()

    for url in bookmarked_articles:
        articles.append(db.get_article(url))

    return articles

def get_liked_articles(db):
    global liked_articles
    print("get_liked_articles")
    articles = []
    if len(liked_articles) == 0:
        liked_articles = local_storage.get_liked_articles()
    
    print(liked_articles)

    for url in liked_articles:
        # print("hey")
        article = db.get_article(url)
        # print(article)
        articles.append(article)

    return articles