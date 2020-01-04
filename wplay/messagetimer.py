import time
import random
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


def msgTimer(name):

    target = str(name)

    # enter message type number
    nMessages = int(input("How many types of messages will you send? "))

    # type your messages
    messages = list()
    for i in range(0, nMessages):
        messages.append(str(input("Enter your message: ")))
    n = int(input("Enter the number of messages to send: "))

    # Enter the time interval of the messages, it will be sent using a random
    # interval. For fixed interval, type the same number.
    minimumTimeInterval = int(
        input("Enter minimum interval number in seconds: "))
    maximumTimeInterval = int(
        input("Enter maximum interval number in seconds: "))

    # chrome driver
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://web.whatsapp.com/")
    wait = WebDriverWait(driver, 600)

    # finds the target and navigate to it
    x_arg = '//span[contains(@title, ' + '"' + target + '"' + ')]'
    person_title = wait.until(
        EC.presence_of_element_located((By.XPATH, x_arg)))
    print(target)
    person_title.click()

    # navigate to text part
    xpath = '//div[@class="_3u328 copyable-text selectable-text"]'
    message_area = wait.until(
        EC.presence_of_element_located((By.XPATH, xpath)))

    # sends random messages multiple times
    random.seed()
    i = 0
    while i < n:
        if not messages:
            break
        else:
            message_area.send_keys(
                messages[random.randrange(0, nMessages)] + Keys.ENTER)
            if minimumTimeInterval != maximumTimeInterval:
                time.sleep(random.randrange(minimumTimeInterval,
                                            maximumTimeInterval))
            else:
                time.sleep(minimumTimeInterval)
        i = i+1
