from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeatifulSoup
import requests

def save(name):
	print("It is for testing purpose only. It is not tested yet. Report a bug if you found any error.")
	# enter the name of the person by the user
	target = str(name) #str(input("Enter the name of target: "))
	#target_email = str(input("Enter the email of the target: "))

	# chrome driver
	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get("https://web.whatsapp.com/")
	wait = WebDriverWait(driver, 600)

	# finds the target and navigate to it
	x_arg = '//span[contains(@title, '+ '"' +target + '"'+ ')]'
	person_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
	print(target)
	person_title.click()

	f=open('messages.txt','w')
	# to catch messages

	page = requests.get("https://web.whatsapp.com/")
	soup = BeatifulSoup(page.content, 'html-parser')

	messages = soup.find_all('div', class_='_1_q7u')
	string_messages = str(messages)
	f.write(messages)
	f.close()