import random

import time
import traceback
from sys import argv
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from src.functions import *
import os
#300 likes/hour
#900 likes/day

THUMBNAIL_CLASS = "_si7dy"
#CARD_CLASS = "_622au _5lms4 _4kplh"
CARD_CLASS = "_622au  _5lms4  _4kplh"
PICTURE_CLASS = "_2di5p"
VIDEO_CLASS = "_7thjo"
FULL_HEART_CLASS = "_8scx2  coreSpriteHeartFull"
EMPTY_HEART_CLASS = "_8scx2 coreSpriteHeartOpen "
#EMPTY_HEART_CLASS = "_8scx2 coreSpriteHeartOpen"
PROFILE_THUMBNAIL_CLASS = "_rewi8"
PROFILE_NAME_NEXT_TO_THUMBNAIL_CLASS = "_eeohz"
PROFILE_PICTURE_CLASS = "_82odm"
LIKES_CLASS = "_nzn1h _gu6vm"
LOGGED_IN_CLASS = "_8scx2 _gvoze coreSpriteDesktopNavProfile"

EXPLORE = "explore"
TAG = "tag"
USER = "user"

BOOT_TIME = (5.320, 7.231)
INIT_TIME = (2.212, 4.754)  # random.uniform(*X)
SKIP_PROBABILITY = .08121
LOOK_AT_PROBABILITY = 0.102
LOOK_AT_TIME = (2.7212, 0.5123)  # abs(random.normalvariate(*X))
BASE_TIME = (2.12, 2.9925)  # random.uniform(*X)
MISTAKE_PROBABILITY = 0.072
PROFILE_PROBABILITY = 0.1
PROFILE_TIME = (2.232, 3.553)  # random.uniform(*X)
PROFILE_MAX_LIKES = (3, 7)  # random.randrange(*X)
DECIDE_QUIT_PROFILE_TIME = (.52921, .999)  # random.uniform(*X)
BACK_TO_DEFAULT_FIRST_TIME = (1.2921, .1553)  # random.uniform(*X)
BACK_TO_DEFAULT_SECOND_TIME = (1.54, 1.00122)  # random.uniform(*X)
STOPPING_PROBABILITY = 0.01
STOPPING_TIME = (1.231, 4 * 60.921)  # random.uniform(*X)
DAY_MAX_LIKES = random.randint(812, 901)
QUERY_MAX_LIKES_OFFSET = (-23, 32)
HOUR_MAX_LIKES = (264, 289)
HOUR_WAIT_TIME = (3923, 6666)
GO_LEFT_PROBABILITY = 0.0823423
SWAP_QUERY_TIME = (10.032, 13.032)

# INIT_TIME = (0, 0) #random.uniform(*X)
# LOOK_AT_TIME = (0, 0)  #abs(random.normalvariate(*X))
# BASE_TIME = (0, 0) #random.uniform(*X)
# PROFILE_TIME = (0, 0) #random.uniform(*X)

FINISHED = 0
PAGE_CRASHED = 1

start_time = None
like_count = 0
like_count_in_hour = 0

current_hour_max_likes = random.randint(*HOUR_MAX_LIKES)

def main():
    print("Feed Me.")
    config_file_path = input().strip()

    if " " in config_file_path:
        print("Configuration file name must not contain spaces")
        exit()

    with open(config_file_path) as f:
        lines = f.readlines()
        if not len(lines) > 1:
            print("Configuration file has incorrect format.")
            exit()
        user_data_dir = lines[1].strip()
        queries = []
        for param in lines[1:]:
            param = param.strip().lower()
            url = ""
            if param == EXPLORE:
                url = "explore/"
            else:
                query_type, target = param.split(" ")
                query_type = query_type.strip()
                target = target.strip()

                if query_type == USER:
                    url = target + "/"
                elif query_type == TAG:
                    url = "explore/tags/" + target + "/"
                else:
                    print("Configuration file has incorrect format.")
                    exit()

            queries.append(url)

    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=" + user_data_dir)
    browser = webdriver.Chrome(os.path.join(os.path.dirname(__file__), 'chromedriver'), chrome_options=chrome_options)
    time.sleep(random.uniform(*BOOT_TIME))
    max_likes_per_query = DAY_MAX_LIKES / len(queries)
    global start_time
    start_time = time.time()
    while True:
        random.shuffle(queries)
        for query in queries:
            start_query(browser, query, max_likes_per_query + random.randint(*QUERY_MAX_LIKES_OFFSET))
            time.sleep(random.uniform(*SWAP_QUERY_TIME))


def start_query(browser, query, max_likes):
    print("Starting query " + query + " for " + str(max_likes) + " likes.")

    error_count = 0
    while error_count <= 1:
        browser.get("https://www.instagram.com/" + query)

        while not browser.find_elements(By.CSS_SELECTOR, "[class='" + LOGGED_IN_CLASS + "']"):
            print("Please log in on Instagram using the opened browser and then press enter here.")
            input()
            browser.get("https://www.instagram.com/" + query)

        result = do_page(browser, max_likes)
        if result == PAGE_CRASHED:
            print("Unexpected problem found, retrying query " + query + ".")
            time.sleep(10)
            error_count += 1
        else:
            break


def do_page(browser, max_likes):
    try:
        query_like_count = 0

        global like_count
        global like_count_in_hour

        time.sleep(random.uniform(*INIT_TIME))

        if browser.find_elements(By.CLASS_NAME, PROFILE_PICTURE_CLASS):
            is_profile = True
        else:
            is_profile = False

        thumbnails = browser.find_elements(By.CLASS_NAME, THUMBNAIL_CLASS)

        if len(thumbnails) == 0:
            print("No more thumbnails")
            return FINISHED

        first_thumbnail = thumbnails[0]
        ActionChains(browser).move_to_element_with_offset(first_thumbnail,
                                                          *get_random_offset_in_picture(
                                                              first_thumbnail)).click().perform()

        wait = ui.WebDriverWait(browser, 20)
        wait.until(lambda driver: browser.find_element(By.CSS_SELECTOR, "[class^='" + CARD_CLASS + "']"))

        first = True

        while True:
            current_time = time.time() - start_time

            skip = False
            if random.random() <= SKIP_PROBABILITY:
                skip = True

            card = browser.find_element(By.CSS_SELECTOR, "[class^='" + CARD_CLASS + "']")

            has_picture = card.find_elements(By.CLASS_NAME, PICTURE_CLASS)
            if has_picture:
                picture = has_picture[0]
                wait = ui.WebDriverWait(browser, 20)
                try:
                    wait.until(lambda driver: driver.execute_script("return arguments[0].complete", picture))
                except:
                    skip = True

            time.sleep(random.uniform(*BASE_TIME))

            if random.random() <= LOOK_AT_PROBABILITY:
                time.sleep(abs(random.normalvariate(*LOOK_AT_TIME)))

            if not skip:
                has_empty_heart = browser.find_elements(By.CSS_SELECTOR, "[class='" + EMPTY_HEART_CLASS + "']")
                if has_empty_heart:
                    empty_heart = has_empty_heart[0]
                    if first:
                        ActionChains(browser).move_to_element_with_offset(empty_heart, *get_random_offset_in_picture(
                            empty_heart)).click().perform()
                        first = False
                    else:
                        webdriver.ActionChains(browser).send_keys(Keys.ENTER).perform()
                    wait = ui.WebDriverWait(browser, 20)
                    wait.until(
                        lambda driver: browser.find_element(By.CSS_SELECTOR, "[class='" + FULL_HEART_CLASS + "']"))
                    like_count += 1
                    like_count_in_hour += 1
                    query_like_count += 1
                elif not first and random.random() <= MISTAKE_PROBABILITY:
                    webdriver.ActionChains(browser).send_keys(Keys.ENTER).perform()
                    wait = ui.WebDriverWait(browser, 20)
                    wait.until(
                        lambda driver: browser.find_element(By.CSS_SELECTOR, "[class='" + EMPTY_HEART_CLASS + "']"))

            if random.random() <= LOOK_AT_PROBABILITY:
                time.sleep(abs(random.normalvariate(*LOOK_AT_TIME)))

            if not is_profile and random.random() <= PROFILE_PROBABILITY:
                time.sleep(random.uniform(*PROFILE_TIME))
                profile = card.find_element(By.CLASS_NAME, PROFILE_NAME_NEXT_TO_THUMBNAIL_CLASS)
                ActionChains(browser).move_to_element_with_offset(profile,*get_random_offset_in_picture(profile)).click().perform()
                wait = ui.WebDriverWait(browser, 20)
                wait.until(lambda driver: is_stale(profile))
                do_page(browser, random.randrange(*PROFILE_MAX_LIKES))
                profile_card = browser.find_element(By.CSS_SELECTOR, "[class^='" + CARD_CLASS + "']")
                time.sleep(random.uniform(*DECIDE_QUIT_PROFILE_TIME))
                browser.back()
                wait = ui.WebDriverWait(browser, 20)
                wait.until(lambda driver: is_stale(profile_card))
                time.sleep(random.uniform(*BACK_TO_DEFAULT_FIRST_TIME))
                browser.back()
                wait.until(lambda browser: browser.find_element(By.CSS_SELECTOR, "[class^='" + CARD_CLASS + "']"))
                profile_card = browser.find_element(By.CSS_SELECTOR, "[class^='" + CARD_CLASS + "']")
                time.sleep(random.uniform(*BACK_TO_DEFAULT_SECOND_TIME))
                first = True

            if query_like_count > max_likes:
                return FINISHED
            if like_count > DAY_MAX_LIKES:
                print("Did " + str(like_count) + " today. Going to stop now. Byes.")
                input()
                exit()

            if like_count_in_hour > current_hour_max_likes:
                hour_wait_time = random.uniform(*HOUR_WAIT_TIME)
                print("Already did " + str(like_count_in_hour) + " likes in the last hour. Going to stop for " + str(hour_wait_time) + " seconds." )
                time.sleep(hour_wait_time)
                print("I'm back.")
                like_count_in_hour = 0

            card = browser.find_element(By.CSS_SELECTOR, "[class^='" + CARD_CLASS + "']")
            old_card = browser.execute_script("return arguments[0].outerHTML", card)
            if random.random() <= GO_LEFT_PROBABILITY:
                webdriver.ActionChains(browser).send_keys(Keys.LEFT).perform()
            else:
                webdriver.ActionChains(browser).send_keys(Keys.RIGHT).perform()

            def is_element_equal(driver):
                new_card = browser.execute_script("return arguments[0].outerHTML", card)
                return old_card == new_card

            if random.random() <= STOPPING_PROBABILITY:
                stop_time = random.uniform(*STOPPING_TIME)
                print("I'm going out for coffee for about " + str(stop_time)+ " seconds, brb. ")
                time.sleep(stop_time)
                print("I'm back.")

            try:
                wait = ui.WebDriverWait(browser, 20)
                wait.until_not(is_element_equal)
            except TimeoutException:
                return FINISHED
            except StaleElementReferenceException:
                return PAGE_CRASHED
    except TimeoutException as e:
        print("Something took more then 10 seconds to load.")
        traceback.print_exc()
        return PAGE_CRASHED


if __name__ == "__main__":
    main()
