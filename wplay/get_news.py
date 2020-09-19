# region IMPORTS
from pathlib import Path
import time

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
    """
    Sends news as a message in every two minutes.
    """
    def fetch_news(country_code):
        """
        Return the title and url of the news.
        """
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
            await io.send_message(page, news_)
        except Exception as e:
            print("Unable to get the news", e)
        time.sleep(120)  # Sends news in every 2 min
