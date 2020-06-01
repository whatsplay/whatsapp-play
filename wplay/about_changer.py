# region IMPORTS
import time
from pathlib import Path
from wplay.utils.helpers import whatsapp_selectors_dict
from wplay.utils import browser_config
from wplay.utils.Logger import Logger
from newsapi.newsapi_client import NewsApiClient
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


# Asking user
async def about_changer():
    option = input("Choose(1/2) \n1.Write new about \n2.Change about with latest headline\n")
    if option == '1':
        await change_about()
    else:
        await about_changer_news()


# Custom About
async def change_about():
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    # opens photo element
    await page.waitForSelector(whatsapp_selectors_dict['profile_photo_element'], visible=True)
    await page.click(whatsapp_selectors_dict['profile_photo_element'])
    await page.waitForSelector(whatsapp_selectors_dict['about_edit_button_element'])
    await page.click(whatsapp_selectors_dict['about_edit_button_element'])
    status = input("Enter your new about: ")
    __logger.info("Writing About")
    # Write about
    await page.type(whatsapp_selectors_dict['about_text_area'], status)
    await page.keyboard.press('Enter')
    print("About changed to {}".format(status))


async def get_api_key():
    __logger.info("Getting key")
    print("Visit https://newsapi.org/ to get your own API key")
    key = input("Enter you API KEY : ")
    get_api_key.newsapi = NewsApiClient(api_key='{}'.format(key))


# News in About
async def about_changer_news():
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    await get_api_key()
    query: str = str(input("What's the news theme? : "))
    # opens photo element
    await page.waitForSelector(whatsapp_selectors_dict['profile_photo_element'], visible=True)
    await page.click(whatsapp_selectors_dict['profile_photo_element'])
    news = ''
    while True:
        current_news = str(fetch_news(query))
        print(current_news)
        if news != current_news:
            # Click on edit about button
            await page.waitForSelector(whatsapp_selectors_dict['about_edit_button_element'])
            await page.click(whatsapp_selectors_dict['about_edit_button_element'])
            for _ in range(140):
                await page.keyboard.press('Backspace')
            news = current_news
            __logger.info("Updating About latest news")
            # Write about
            await page.type(whatsapp_selectors_dict['about_text_area'], news)
            await page.keyboard.press('Enter')
        # News get updated every 15 minutes by newsapi.org
        # Added extra minute for buffer period
        # For free account : max limit is 500 request/day
        time.sleep(905)


def fetch_news(query):
    __logger.info("Fetching news")
    top_headlines = get_api_key.newsapi.get_top_headlines(q=query, language='en')
    return top_headlines['articles'][0]['title']
