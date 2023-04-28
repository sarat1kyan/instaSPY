import time
import os
import sys
import time
import getpass
import requests
import json
import webbrowser
from datetime import datetime, timedelta
from collections import Counter
from InstagramAPI import InstagramAPI

try:
    from bs4 import BeautifulSoup
    import selenium
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
except ImportError:
    print("Some modules are not installed. Would you like to install them now? (Y/N)")
    choice = input().lower()
    if choice == 'y':
        os.system('sudo apt-get update')
        os.system('sudo apt-get install python3-pip -y')
        os.system('sudo pip3 install beautifulsoup4')
        os.system('sudo pip3 install selenium')
        os.system('sudo pip3 install requests')
        os.system('sudo pip3 install webdriver_manager')
        from bs4 import BeautifulSoup
        import selenium
        from selenium import webdriver
        from selenium.webdriver.common.keys import Keys
        from selenium.webdriver.common.action_chains import ActionChains
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
    else:
        print("Please install the missing modules first.")
        sys.exit()

# Set up the driver and wait for elements to load
def start_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)
    return driver, wait

# Login to Instagram
def login(driver, wait, username, password):
    driver.get("https://www.instagram.com/accounts/login/")
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
    username_input = driver.find_element_by_xpath("//input[@name='username']")
    password_input = driver.find_element_by_xpath("//input[@name='password']")
    username_input.send_keys(username)
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='glyphsSpriteUser__outline__24__grey_9 u-__7']")))


# Get the Instagram account's follower list
def get_followers_list(api, instagram_username):
    api.searchUsername(instagram_username)
    user_id = api.LastJson['user']['pk']
    api.getUserFollowers(user_id)
    followers = [user['username'] for user in api.LastJson['users']]
    return followers

# Get the list of users who are followed by the Instagram account
def get_following_list(api, instagram_username):
    api.searchUsername(instagram_username)
    user_id = api.LastJson['user']['pk']
    api.getUserFollowings(user_id)
    followings = [user['username'] for user in api.LastJson['users']]
    return followings

# Get the list of users who have liked the posts of the Instagram account
def get_likers_list(api, instagram_username):
    api.searchUsername(instagram_username)
    user_id = api.LastJson['user']['pk']
    api.getUserFeed(user_id)
    likers = []
    for post in api.LastJson['items']:
        api.getMediaLikers(post['id'])
        likers += [user['username'] for user in api.LastJson['users']]
    likers_count = Counter(likers)
    return likers_count

# Get the list of users who have commented on the posts of the Instagram account
def get_commenters_list(api, instagram_username):
    api.searchUsername(instagram_username)
    user_id = api.LastJson['user']['pk']
    api.getUserFeed(user_id)
    commenters = []
    for post in api.LastJson['items']:
        api.getMediaComments(post['id'])
        commenters += [comment['user']['username'] for comment in api.LastJson['comments']]
    commenters_count = Counter(commenters)
    return commenters_count

# List the top 5 users who have liked the posts of the provided username
def get_top_likers(api, instagram_username, provided_username):
    api.searchUsername(instagram_username)
    user_id = api.LastJson['user']['pk']
    api.getUserFeed(user_id)
    likers = []
    for post in api.LastJson['items']:
        api.getMediaLikers(post['id'])
        likers += [user['username'] for user in api.LastJson['users'] if user['username'] == provided_username]
    likers_count = Counter(likers)
    top_likers = likers_count.most_common(5)
    return top_likers

# List the top users who have commented on the posts of the provided username
def get_top_commenters(api, instagram_username, provided_username):
    api.searchUsername(instagram_username)
    user_id = api.LastJson['user']['pk']
    api.getUserFeed(user_id)
    commenters = []
    for post in api.LastJson['items']:
        api.getMediaComments(post['id'])
        commenters += [comment['user']['username'] for comment in api.LastJson['comments'] if comment['user']['username'] == provided_username]
    commenters_count = Counter(commenters)
    top_commenters = commenters_count.most_common()
    return top_commenters

# Check if the provided usernames are following each other
def check_follows_each_other(instagram_username, other_username):
    """
    Check if the provided usernames are following each other.

    Args:
    - instagram_username (str): The Instagram username to check.
    - other_username (str): The other Instagram username to check.

    Returns:
    - str: A string indicating whether the provided usernames follow each other or not.
    """
    try:
        instagram_user = instaloader.Profile.from_username(context, instagram_username)
        other_user = instaloader.Profile.from_username(context, other_username)

        if instagram_user.is_following(other_user) and other_user.is_following(instagram_user):
            return f"{instagram_username} and {other_username} follow each other."
        else:
            return f"{instagram_username} and {other_username} do not follow each other."
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def check_blocked_by_user(instagram_username, other_username, password):
    """
    Check if the provided Instagram username is blocked by the other provided Instagram username.

    Args:
    - instagram_username (str): The Instagram username to check.
    - other_username (str): The other Instagram username to check.
    - password (str): The password of the provided Instagram username.

    Returns:
    - str: A string indicating whether the provided Instagram username is blocked or not.
    """
    try:
        L = instaloader.Instaloader()
        L.load_session_from_file(instagram_username)
        profile = instaloader.Profile.from_username(L.context, other_username)

        if profile.is_blocked_by_viewer:
            return f"{instagram_username} is blocked by {other_username}."
        else:
            return f"{instagram_username} is not blocked by {other_username}."
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def check_new_story(instagram_username, password):
    """
    Check every 10 seconds and notify if a new story is uploaded by the provided Instagram username.

    Args:
    - instagram_username (str): The Instagram username to check.
    - password (str): The password of the provided Instagram username.
    """
    try:
        L = instaloader.Instaloader()
        L.load_session_from_file(instagram_username)

        while True:
            profile = instaloader.Profile.from_username(L.context, instagram_username)
            stories = profile.get_stories()
            if stories:
                print("New story uploaded!")
                notify("New story uploaded!", "Check your Instagram account.")
            time.sleep(10)
    except Exception as e:
        print(f"An error occurred: {e}")


def get_inactive_following(instagram_username, password):
    """
    Get a list of accounts that the provided Instagram username is following but hasn't interacted with in a while.

    Args:
    - instagram_username (str): The Instagram username to check.
    - password (str): The password of the provided Instagram username.

    Returns:
    - list: A list of Instagram usernames that the provided Instagram username follows but hasn't interacted with in a while.
    """
    try:
        L = instaloader.Instaloader()
        L.load_session_from_file(instagram_username)
        profile = instaloader.Profile.from_username(L.context, instagram_username)
        following = []
        for followee in profile.get_followees():
            if followee.has_liked_recently:
                following.append(followee.username)
        return following
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def remove_fake_followers(api):
    followers = api.get_user_followers()
    fake_followers = []
    for user in followers:
        if user["is_private"] or user["follower_count"] > 10000:
            # If the account is private or has a suspiciously high number of followers
            fake_followers.append(user["pk"])
    if fake_followers:
        print(f"Found {len(fake_followers)} fake/spam accounts")
        api.block_users(fake_followers)
    else:
        print("No fake/spam accounts found")
