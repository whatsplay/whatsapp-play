from wplay.utils.helpers import whatsapp_selectors_dict
from wplay.utils import browser_config
import time
import sys
import requests

async def changeAbout():
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    choice = input("Choose 1 for changing About section every second and 2 for changing About in every 30 min : ")
    if choice not in ['1', '2']:
        print("Wrong choice")
        sys.exit()
    await page.waitForSelector(
        whatsapp_selectors_dict['profile_photo_element'],
        visible=True
    )
    await page.click(whatsapp_selectors_dict['profile_photo_element'])

    while True:
        await page.waitForSelector(whatsapp_selectors_dict['about_edit_button_element'])
        await page.click(whatsapp_selectors_dict['about_edit_button_element'])
        for _ in range(140):
            await page.keyboard.press('Backspace')
        await page.type(whatsapp_selectors_dict['about_text_area'], get_live_cases())
        await page.keyboard.press('Enter')
        if choice == '1':
            time.sleep(1)
        else:
            time.sleep(1800)

def get_live_cases():
    '''
    Gives total cases live in world for coronavirus(IN)
    '''
    URL = "https://thevirustracker.com/free-api?global=stats"
    data = requests.get(URL).json()

    live_cases = data['results'][0]['total_cases']
    return str("Total Coronavirus Cases: " + str(live_cases))
