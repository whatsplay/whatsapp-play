from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import target_select
from wplay.utils import io
import requests
import time

async def get_news(target):
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    if target is not None:
        try:
            await target_search.search_and_select_target(page, target)
        except Exception as e:
            print(e)
            await target_search.search_and_select_target_without_new_chat_button(page, target)
    else:
        await target_select.manual_select_target(page)
    
    country = input("Enter your country code: ")
    while True:
        try:
            news, source = fetch_news(country)
            news_ = f"*{news}* \n Full News :  {source}"
        except Exception as e:
            print("Unable to get the news", e)
        await io.send_message(page, news_)
        time.sleep(900) # Sends news in every 15 min


def fetch_news(country_code):
    try:
        data = requests.get(f"https://thevirustracker.com/free-api?countryNewsTotal={country_code}", headers={"User-Agent": "XY"}).json()
        news = data['countrynewsitems'][0]['1']['title']
        source = data['countrynewsitems'][0]['1']['url']
        return news, source
    except:
        return "Sorry", "Unable to fetch news"
