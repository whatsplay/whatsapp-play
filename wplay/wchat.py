# These are imports from util folder of wplay
from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import io

# First checks for the target which is the username as entered by the client after running wplay on a command line script
async def chat(target):
    page, _ = await browser_config.configure_browser_and_load_whatsapp()

    await target_search.search_and_select_target(page, target)
    
    # If all the configurations are correct whatsapp web is loaded and target found then ask for message and send message.
    while True:
        message = io.ask_user_for_message_breakline_mode()
        await io.send_message(page, message)
