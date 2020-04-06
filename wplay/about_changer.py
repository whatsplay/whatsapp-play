# region IMPORTS
import time
import os
import sys

from newsapi.newsapi_client import NewsApiClient
import requests
from dotenv import load_dotenv

from wplay.utils.helpers import whatsapp_selectors_dict
from wplay.utils import browser_config
# endregion

load_dotenv()
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))


async def about_changer():
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    query: str = str(input("What's the news theme? : "))

    await page.waitForSelector(
        whatsapp_selectors_dict['profile_photo_element'],
        visible=True
    )
    await page.click(whatsapp_selectors_dict['profile_photo_element'])
    news = ''
    while True:
        current_news = str(fetch_news(query))
        print(current_news)
        if news != current_news:
            await page.waitForSelector(whatsapp_selectors_dict['about_edit_button_element'])
            await page.click(whatsapp_selectors_dict['about_edit_button_element'])
            for _ in range(140):
                await page.keyboard.press('Backspace')
            news = current_news
            await page.type(whatsapp_selectors_dict['about_text_area'], news)
            await page.keyboard.press('Enter')
        # News get updated every 15 minutes by newsapi.org
        # Added extra minute for buffer period
        # For free account : max limit is 500 request/day
        time.sleep(905)


def fetch_news(query):
    top_headlines = newsapi.get_top_headlines(q=query, language='en')
    return top_headlines['articles'][0]['title']
