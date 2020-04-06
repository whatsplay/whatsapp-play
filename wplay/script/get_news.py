# region IMPORTS
from pathlib import Path
import time
import os

from dotenv import load_dotenv
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


load_dotenv()
newsapi = NewsApiClient(api_key=os.getenv("NEWS_API_KEY"))


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
    
    country = input("Enter your country code (ex: us or in): ")
    while True:
        try:
            news, source = fetch_news(country)
            news_ = f"*{news}* \n Full News :  {source}"
        except Exception as e:
            print("Unable to get the news", e)
        await io.send_message(page, news_)
        time.sleep(900) # Sends news in every 15 min
