from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


print("* * *    *      * * *  *    *  * * *     * * *  *    *  * * *")
print("*    *   *        *    * *  *  *    *    *       *  *   *    ")
print("* * *    *        *    *  * *  *     *   * *      **    * *  ")
print("*    *   *        *    *   **  *    *    *        *     *    ")
print("* * *    * * *  * * *  *    *  * * *     * * *   *      * * *")

# enter the number of the person by the user
target = str(input("Enter the name of target: "))

# chrome driver
chrome_options = Options()
driver = webdriver.Chrome('/home/rohit/blind-eye/chromedriver')
driver.get("https://web.whatsapp.com/")
wait = WebDriverWait(driver, 600)
assert "WhatsApp" in driver.title

# finds the target and navigate to it
x_arg = '//span[contains(@title, '+ '"' +target + '"'+ ')]'
print(x_arg)
person_title = wait.until(EC.presence_of_element_located((
    By.XPATH, x_arg)))
print(person_title)
person_title.click()

# check status
while True:
	online = driver.find_element_by_class_name('O90ur').text
	if online == 'online':
		print(TARGET + ' is online!')
	else:
		print("offline")
	time.sleep(5)