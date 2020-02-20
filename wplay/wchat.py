from wplay.utils import pyppeteerConfig as pypConfig
from wplay.utils import pyppeteerSearch as pypSearch
from wplay.utils import pyppeteerIO as pypIO

async def chat(target):
    #target = str(input("Enter the name of target: "))
    pages, browser = await pypConfig.configure_browser_and_load_whatsapp(pypConfig.websites['whatsapp'])
    await pypSearch.search_for_target_and_get_ready_for_conversation(pages[0], target)
    
    try:
        while True:
            #message = pypIO.ask_user_for_message()
            message = pypIO.ask_user_for_message_breakline_mode()
            await pypIO.send_message(pages[0], message)
    except:
        await browser.close()
