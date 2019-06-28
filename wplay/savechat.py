from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime
import os
import sys

def save(name):
	script_path = sys.path[0]

	# enter the name of the person by the user
	target = str(name) #str(input("Enter the name of target: "))
	#target_email = str(input("Enter the email of the target: "))

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

	f=open('messages.txt','w')
	f.close()
	# to catch messages
	while True:
		try:
			time=driver.find_element_by_class_name('copyable-text').text
			messages=driver.find_element_by_class_name('selectable-text invisible-space copyable-text ').text
			f=open('status.txt','a')
			f.write(time+" : "+messages)
			f.close()
		except (NoSuchElementException):
			break;
