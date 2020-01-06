import time
import os
import datetime
from playsound import playsound
from wplay import seleniumUtils as sel

def tracker(name):

    # the name of the person by the user
    target = str(name) #str(input("Enter the name of target: "))

    driver, driver_wait, chosen_website = sel.initialize_chrome_driver(
        sel.websites['whatsapp'])

    sel.find_and_navigate_to_target(driver_wait, chosen_website, target)

    NoSuchElementException, \
		StaleElementReferenceException = sel.get_selenium_exceptions()

    # finds if online_status directory is present
    if 'online_status_data' not in os.listdir(os.getcwd()):
        os.mkdir('online_status_data')
    f=open(os.path.join('online_status_data' , 'status.txt'),'w')
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
        # to play sound when the person is online
        if i==1:
            try:
                playsound('plucky.wav')
            except:
                print("Error: Couldn't play the sound. \
                But the person is online!")
        # prints date, time and status
        print(datetime.datetime.now())
        print(status)
        # writes date, time and status in status.txt
        f=open(os.path.join('online_status_data' , 'status.txt'),'a')
        f.write(str(datetime.datetime.now()))
        f.write(status)
        f.close()
        # Loop to check the online status until the offline status appear and vice-versa
        # this loop will help to stop print status until the other status appears
        while True:
            if i == 1:
                try:
                    re_status = driver.find_element_by_class_name('_315-i').text
                    re_status = 'online'
                    continue
                except (NoSuchElementException, StaleElementReferenceException):
                    break
            else:
                try:
                    re_status = driver.find_element_by_class_name('_315-i').text
                    re_status = 'online'
                    break
                except (NoSuchElementException, StaleElementReferenceException):
                    continue
        time.sleep(1)
