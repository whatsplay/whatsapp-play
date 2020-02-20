from wplay.utils import pyppeteerConfig as pypConfig
from wplay.utils import pyppeteerSearch as pypSearch
from wplay.utils import pyppeteerIO as pypIO

async def blast(target):
    #target = str(input("Enter the name of target: "))
    
    pages, browser = await pypConfig.configure_browser_and_load_whatsapp(pypConfig.websites['whatsapp'])
    
    try:
        await pypSearch.search_for_target_and_get_ready_for_conversation(pages[0], target)

        #message = pypIO.ask_user_for_message()
        message = pypIO.ask_user_for_message_breakline_mode()

        number_of_messages = int(input("Enter the number of messages to blast: "))

        for _ in range(number_of_messages):
            await pypIO.send_message(pages[0], message)
    except:
        await browser.close()
