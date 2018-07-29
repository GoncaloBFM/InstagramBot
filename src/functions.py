import random

from selenium.common.exceptions import StaleElementReferenceException, TimeoutException


def is_stale(element):
    try:
        element.is_displayed()
        return False
    except StaleElementReferenceException:
        return True


def wait_till_not_stale(element, wait):
    try:
        wait.until(lambda driver: is_stale(element))
        return True
    except TimeoutException:
        return False


def get_random_offset_in_picture(element):
    return random.uniform(0, element.size["width"]), random.uniform(0, element.size["height"])
