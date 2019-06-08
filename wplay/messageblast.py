from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import os
import sys

def blast(name):
	script_path = sys.path[0]

	# enter the number of the person by the user
	target = str(name) #str(input("Enter the name of target: "))
	message = str(input("Enter your message: "))
	n = int(input("Enter the number of messages to blast: "))

	# chrome driver
	chrome_options = Options()
	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get("https://web.whatsapp.com/")
	wait = WebDriverWait(driver, 600)
	assert "WhatsApp" in driver.title

	# finds the target and navigate to it
	x_arg = '//span[contains(@title, '+ '"' +target + '"'+ ')]'
	person_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
	print(target)
	person_title.click()

	# navigate to text part
	xpath = '//div[@class="_3u328 copyable-text selectable-text"]'
	message_area = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

	# sends message multiple times
	for i in range(n):
		message_area.send_keys(message + Keys.ENTER)
