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

def tracker(name):
	script_path = sys.path[0]

	# enter the name of the person by the user
	target = str(name) #str(input("Enter the name of target: "))

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

	f=open('status.txt','w')
	f.close()
	# check status
	while True:
		i=0
		try:
			status = driver.find_element_by_class_name('_315-i').text
			i=1
		except (NoSuchElementException, StaleElementReferenceException):
			status = 'offline'
			i=0
		print(datetime.datetime.now())
		print(status)
		f=open('status.txt','a')
		f.write(str(datetime.datetime.now()))
		f.write(status)
		f.close()
		while True:
			if i == 1:
				try:
					re_status = driver.find_element_by_class_name('_315-i').text
					continue
				except (NoSuchElementException, StaleElementReferenceException):
					re_status = 'offline'
					break
			else:
				try:
					re_status = driver.find_element_by_class_name('_315-i').text
					break
				except (NoSuchElementException, StaleElementReferenceException):
					re_status = 'offline'
					continue
		time.sleep(1)
