# selenium imports


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Other imports
import os
import shutil
import time
import json
import requests as r


# Json functions for saving, and retrieving saved variables
def set_variables(user_name_var: str = "",
                  password_var: str = "",
                  download_dir: str = "",
                  last_search: str = "",
                  download_count: int = 0,
                  last_scroll: int = 0):

    defaults = {}
    driver_dir = os.getcwd()
    driver_dir = driver_dir[driver_dir.find("C:"):] + '\chromedriver.exe'
    driver_dir = driver_dir.replace("\\", "/")
    # Must Pass 3 Args for setting variables, if not changing
    # a value call get_X() for each value not changing
    if user_name_var != "" and password_var != "" and download_dir != '':
        defaults = {"username": user_name_var,
                    "password": password_var,
                    "download_dir": download_dir,
                    "driver_dir": driver_dir,
                    "last_search": get_last_search(),
                    "download_count": get_last_download_count(),
                    "Last_scroll_count": get_last_scroll_start()}
    # To update the download numbers so if you start over on a specific
    # search term it will pick up where you left off
    elif user_name_var == "" and password_var == "" and download_dir == "":
        defaults = {"username": get_username(),
                    "password": get_password(),
                    "download_dir": get_last_download_dir(),
                    "driver_dir": get_driver(),
                    "last_search": last_search,
                    "download_count": download_count,
                    "last_scroll_count": last_scroll}
    with open(".\sys_variables.json", "w") as f:
        json.dump(defaults, f)
    # display_variables()


def display_variables():
    with open("sys_variables.json", "r") as f:
        var = json.load(f)
        print(f"\nGLOBAL VARIABLES:\n\nUsername: {var.get('username')}\n"
              f"Password: {'*' * len(var.get('password'))}\n"
              f"Driver Path: {var.get('driver_dir')}\n"
              f"Current Download Directory: {var.get('download_dir')}", flush=True)


# Functions for pulling global variables to pass into set_variables
def get_username() -> str:
    with open("sys_variables.json", "r") as f:
        var = json.load(f)
    return var.get("username")


def get_password() -> str:
    with open("sys_variables.json", "r") as f:
        var = json.load(f)
    return var.get("password")


def get_driver() -> str:
    with open("sys_variables.json", "r") as f:
        var = json.load(f)
    return var.get("driver_dir")


def get_last_download_dir() -> str:
    with open("sys_variables.json", "r") as f:
        var = json.load(f)
    return var.get("download_dir")


def get_last_download_count() -> int:
    with open("sys_variables.json", "r") as f:
        var = json.load(f)
    return var.get("download_count")


def get_last_search() -> str:
    with open("sys_variables.json", "r") as f:
        var = json.load(f)
    return var.get("last_search")


def get_last_scroll_start() -> int:
    with open("sys_variables.json", "r") as f:
        var = json.load(f)
    return var.get("last_scroll_count")


# Introduction
print("""

ZUXX_TA_GRAM: A Selenuim Webdriver based instagram scraper.

This script will automate the downloading 
of images for the specific hashtags on *users 

Requirements:

    Chrome version Version 100.0.4896.88

    An Instagram account

    On initial use you will be prompted to enter your login 
info for your Instagram which will be saved in a file in this 
program's source folder. It could be possible for someone to 
access this information by viewing the Json file in the program 
folder, so a "burner" account is recommended. 

    Once the script has saved your information you can change it 
in the startup prompt by typing 'wipe'. This script will also ask you for the 
file path for download content. every new search will generate 
a folder with a corresponding name to your search term.
You will be prompted on startup if you would like to change 
this directory.

After all variables have been satisfied you will be prompted for 
a search term and a number of photos you would like to save. While 
I have used this script in testing to save as many as 10k photos 
this is not recommended. generally about 1000 photos is a good number.
the script will auto scroll and cache the urls of each photo until the 
requested number of downloads has been reached/exceeded. then it will 
start the download of the entire batch of saved urls one at a time.
Each photo will be saved with a name of the hashtag and a number. 
You may download batches of photos from the same hashtag/user 
after the fist batch of

*(provided you know their names and those names 
are unique enough to be found via search as a first result. 
if you follow those users you will have a higher rate of 
success with this)

**(if you have a newer version locate and replace the 
chromedriver.exe file in the program folder with the 
version that corresponds with your current version of 
Google Chrome.)
""")

# set globals
if get_password() == "" or get_username() == "":
    init_username = input("\nInput your Instagram Username: \n > ")
    init_password = input("\nInput your Instagram Password: \n > ")
    init_download_dir = input("\nEnter your download directory:\n > ")
    set_variables(init_username, init_password, init_download_dir)
    display_variables()
if get_last_download_dir() != '':
    download_set = input(f"\nyour current download directory is: {get_last_download_dir()}"
                         f"\nWould you like to change it?\n(y/n): > ")
    if download_set.find('y') != -1:
        init_download_dir = input("\nEnter your download directory:\n > ")
        set_variables(get_username(), get_password(), init_download_dir)
        # wipe function
        # exit(code="Global variables reset")


display_variables()
# user input variables:
print(f"\nLast search: '{get_last_search()}'")
search_username_or_hashtag = input("Enter Your search term (if its a hashtag, please include the '#')\nTerm: > ")
number_of_photos_to_download = input("\nEnter the number of photos you'd like to download. \nNumber of photos: > ")
continue_download = ""

# Assigning Login info
instagram_username = get_username()
instagram_password = get_password()

# Initializing the WebDriver
driver = webdriver.Chrome(get_driver())
driver.get("https://www.instagram.com/")
try:
    cookies = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Only allow essential cookies")]'))).click()
except TimeoutException:
    print("no cookies this time")
username = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username")))
password = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password")))

# Entering Username and Passwords
username.clear()
password.clear()
username.send_keys(instagram_username)
password.send_keys(instagram_password)

# Login Button Press
log_in = WebDriverWait(driver, 10).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit"))).click()

# By passing the Buttons
not_now = WebDriverWait(driver, 10).until(
    ec.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()
not_now2 = WebDriverWait(driver, 10).until(
    ec.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Not Now")]'))).click()

while continue_download.find("n") == -1:
    keyword = ""
    continuing = False
    if continue_download == "y":
        print("\nYou may enter a new search term, \nor press ENTER to download more photos from this page.\n")
        search = input("Enter Your search term (if a hashtag, include the '#')\nNew Term or hit Enter > ")
        if search == "":
            continuing = True
            search_username_or_hashtag = search
        elif search != '':
            search_username_or_hashtag = search
            continuing = False
        number_of_photos_to_download = input("\nEnter the number of photos you'd like to download: \n > ")

    if not continuing:
        # Entering the search term in the search window
        search_box = WebDriverWait(driver, 10).until(
            ec.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search']")))
        search_box.clear()
        keyword = search_username_or_hashtag
        search_box.send_keys(search_username_or_hashtag)
        time.sleep(1.5)

        # Hitting the search enter key 2x (sometimes once won't work properly)
        search_box.send_keys(Keys.ENTER)
        time.sleep(1)
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)

    # declaring variables to harvest images as we scroll
    # setting the counts if continuing on the same page
    image_cache = []
    scroll_start = 0
    scroll_counter = 0
    scroll_forward = 4000
    scroll_last = False
    if continuing:
        time.sleep(5)
        driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)
        scroll_start = get_last_scroll_start()
        scroll_forward = scroll_start + 4000
    scrape_check_count = 0

    while len(image_cache) < int(number_of_photos_to_download):
        scrape_check_len = len(image_cache)
        driver.execute_script(f"window.scrollTo({scroll_start}, {scroll_forward});")
        time.sleep(1)
        driver.execute_script(f"window.scrollTo({scroll_forward / 2}, {scroll_forward / 2});")
        scroll_start = scroll_forward
        scroll_forward += 4000
        time.sleep(5)
        images = driver.find_elements(by=By.TAG_NAME, value='img')
        images = [image.get_attribute('src') for image in images]
        for image in images:
            if image_cache.count(image) == 0:
                image_cache += [image]
        print(f"Number of scrolls {scroll_counter}. Number of pictures queued: {len(image_cache)}.")

        # a block to stop it scrolling if it hits the end of the page
        scroll_counter += 1
        if scrape_check_len == len(image_cache):
            scrape_check_count += 1
            if scrape_check_count >= 3:
                break

    path = get_last_download_dir()
    if keyword.find("#") == -1:
        path = path + "\\" + keyword
    else:
        path = path + "\\" + keyword[1:]

    # if not continuing:
    try:
        os.mkdir(path)
    except OSError:
        print(f"Adding files to {path}\n")
    print(f"\nStarting Download to: {path}")

    if continuing:
        counter = int(get_last_download_count()) + 1
    else:
        counter = 0
    for image in image_cache:
        save_as = path + '\\' + keyword + keyword[1:] + str(counter) + '.jpg'
        # save_as = os.path.join(path, keyword[1:] + str(counter) + '.jpg')
        response = r.get(image, stream=True)
        if response.status_code == 200:
            response.raw.decode_content = True
            with open(save_as, "wb") as f:
                shutil.copyfileobj(response.raw, f)
        # wget.download(image, save_as)
        counter += 1

    set_variables("", "", "", keyword, counter, scroll_start)
    print(f"\nDownloaded {get_last_download_count()} photos to {path}")
    continue_download = input("\nContinue? \n(y/n) > ")
set_variables(get_username(), get_password(), get_last_download_dir())
exit("Goodbye!")
