# region IMPORTS
from pathlib import Path
import time
import os
import win32gui, win32con

from newsapi.newsapi_client import NewsApiClient

from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import target_select
from wplay.utils import io
from wplay.utils.Logger import Logger
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion

'''
Visit https://newsapi.org/ to get your own API key.
'''
newsapi = NewsApiClient(api_key="YOUR API KEY")

async def get_news(target):
    def fetch_news(country_code):
        headlines = newsapi.get_top_headlines(country=country_code, language='en')
        url = headlines['articles'][0]['url']
        title = headlines['articles'][0]['title']
        return title, url

    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    if target is not None:
        try:
            await target_search.search_and_select_target(page, target)
        except Exception as e:
            print(e)
            await target_search.search_and_select_target_without_new_chat_button(page, target)
    else:
        await target_select.manual_select_target(page)

    #Minimizing the Window after Target Select
    print("Browser Minimized")
    Minimize = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(Minimize, win32con.SW_MINIMIZE)

    country = input("Enter your country code (ex: us or in): ")
    while True:
        try:
            news, source = fetch_news(country)
            news_ = f"*{news}* \n Full News :  {source}"
            await io.send_message(page, news_)
        except Exception as e:
            print("Unable to get the news", e)
        time.sleep(120)  # Sends news in every 2 min
