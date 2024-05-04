from js import localStorage
from pyweb import pydom
from Article import *
import json
import local_storage

# This file contains functions relating to action buttons

# Toggle the like button (and possibly the dislike button) visuals and update localStorage
# Input: liked list, disliked list, URL string, like <button>, like <img>, dislike <button>, dislike <image>
def toggle_like(liked_articles, disliked_articles, selected_url, selected_button, selected_img, dislike_button, dislike_img):
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
def toggle_dislike(disliked_articles, liked_articles, selected_url, selected_button, selected_img, like_button, like_img):
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