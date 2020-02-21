from wplay.utils import pyppeteerConfig as pypConfig
from wplay.utils import pyppeteerSearch as pypSearch
from wplay.utils import pyppeteerIO as pypIO

async def chat(target):
    #target = str(input("Enter the name of target: "))
    page, _ = await pypConfig.configure_browser_and_load_whatsapp()

    #await pypSearch.search_for_target_simple(page, target)
    await pypSearch.search_for_target_complete(page, target)

    while True:
        #message = pypIO.ask_user_for_message()
        message = pypIO.ask_user_for_message_breakline_mode()
        await pypIO.send_message(page, message)
