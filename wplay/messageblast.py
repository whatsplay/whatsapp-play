# Importing the various python files present in util folder of wplay
from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import io
# This function gets the input which is username as given by the client and checks for chromedriver to load Whatsapp web.
async def blast(target):
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
# It searches the username by putting the name in search bar by using divison selectors and if more username found asks for your target.
    await target_search.search_and_select_target(page, target)
    message = io.ask_user_for_message_breakline_mode() 
    number_of_messages = int(input("Enter the number of messages to blast: "))  
# Finally it asks for no of message and timing of the messages to the target.
    for _ in range(number_of_messages):
        await io.send_message(page, message)
