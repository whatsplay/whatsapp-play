import sys
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,\
    StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

websites = {'whatsapp': 'https://web.whatsapp.com/'}


def __get_XPATH_list(target=' '):
    XPATH_list = {
        'wpp_target_title': f'//span[contains(@title, "{target}")]',
        'wpp_message_area': '//div[@class="_3u328 copyable-text selectable-text"]'
    }
    return XPATH_list


def initialize_chrome_driver(website_url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(website_url)
    driver_wait = WebDriverWait(driver, 600)
    chosen_website = website_url
    return driver, driver_wait, chosen_website


def find_and_navigate_to_target(driver_wait, chosen_website, target):
    XPATH_list = __get_XPATH_list(target)
    print(f'Looking for: {target}')
    if chosen_website == websites['whatsapp']:
        person_title = driver_wait.until(
            EC.presence_of_element_located((
                By.XPATH, XPATH_list['wpp_target_title'])))
        person_title.click()
        print(f'{target} finded!')
    else:
        sys.exit()


def navigate_to_message_area(driver_wait, chosen_website):
    XPATH_list = __get_XPATH_list()
    if chosen_website == websites['whatsapp']:
        message_area = driver_wait.until(
            EC.presence_of_element_located((
                By.XPATH, XPATH_list['wpp_message_area'])))
    else:
        sys.exit()
    return message_area


def send_message(message_area, message):
    message_area.send_keys(message + Keys.ENTER)


def get_selenium_exceptions():
    return NoSuchElementException, StaleElementReferenceException
