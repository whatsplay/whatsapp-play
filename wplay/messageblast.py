from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import io


async def blast(target):
    #target = str(input("Enter the name of target: "))
    
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    
    #await target_search.search_for_target_simple(page, target)
    await target_search.search_for_target_complete(page, target)

    #message = io.ask_user_for_message()
    message = io.ask_user_for_message_breakline_mode()

    number_of_messages = int(input("Enter the number of messages to blast: "))

    for _ in range(number_of_messages):
        await io.send_message(page, message)
