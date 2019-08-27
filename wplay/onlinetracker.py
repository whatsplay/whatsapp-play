from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from playsound import playsound
import time
import os
import datetime

def tracker(name):

	# enter the name of the person by the user
	target = str(name) #str(input("Enter the name of target: "))

	# chrome driver
	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.get("https://web.whatsapp.com/")
	wait = WebDriverWait(driver, 600)

	# finds the target and navigate to it
	x_arg = '//span[contains(@title, '+ '"' +target + '"'+ ')]'
	person_title = wait.until(EC.presence_of_element_located((By.XPATH, x_arg)))
	print(target)
	person_title.click()

	# finds if online_status directory is present
	if 'online_status_data' not in os.listdir(os.getcwd()):
		os.mkdir('online_status_data')
	f=open(os.path.join('online_status_data' , 'status.txt'),'w')
	f.close()
	# check status and delivers result after every one minute
	start = time.time()
	cnt = 0
	timer_on = False

	while True:
		if timer_on :
			cnt += time.time() - start
		start = time.time()
		try:
			status = driver.find_element_by_class_name('_315-i').text
			if len(status) > 1 and (cnt >= 60 or cnt == 0):
				keep_track = input('The user seems to be offline now, do you wish to keep tracking?[Y/N]')
				if keep_track == 'Y':
					timer_on = True
					continue
				else:
					break
			else:
				playsound('plucky.mp3')
				print('The user is online now! Go, chat :D')
				break
		except (NoSuchElementException, StaleElementReferenceException):
			status = 'offline'
			if  cnt >= 5 or cnt == 60:
				keep_track = input('The user seems to be offline now, do you wish to keep tracking?[Y/N]')
				if keep_track == 'Y':
					timer_on = True
					continue
				else:
					break
		print(datetime.datetime.now())
		print(status)
		f=open(os.path.join('online_status_data' , 'status.txt'),'a')
		f.write(str(datetime.datetime.now()))
		f.write(status)
		f.close()