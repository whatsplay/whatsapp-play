from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException,\
    StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

websites = {'whatsapp': 'https://web.whatsapp.com/'}


def get_XPATH_list(target=' '):
    XPATH_list = {'wpp_target_title': f'//span[contains(@title, "{target}")]',
                  'wpp_message_area': '//div[@class="_3u328 copyable-text selectable-text"]'}
    return XPATH_list


def initialize_chrome_driver(website_url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(website_url)
    wait = WebDriverWait(driver, 600)


def find_and_navigate_to_target(target):
    XPATH_list = get_XPATH_list(target)
    print(f'Looking for: {target}')
    person_title = wait.until(
        EC.presence_of_element_located((
            By.XPATH, XPATH_list['wpp_target_title'])))
    person_title.click()
    print(f'{target} finded!')


def navigate_to_message_area():
    XPATH_list = get_XPATH_list()
    message_area = wait.until(
        EC.presence_of_element_located((
            By.XPATH, XPATH_list['wpp_message_area'])))
    return message_area


def send_message(message_area, message):
    message_area.send_keys(message + Keys.ENTER)
