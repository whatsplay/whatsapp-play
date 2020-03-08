from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import target_select
from wplay.utils import io


async def blast(target):
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    if target is not None:
        await target_search.search_and_select_target(page, target)
    else:
        await target_select.manual_select_target(page)
    message = io.ask_user_for_message_breakline_mode()
    number_of_messages = int(input("Enter the number of messages to blast: "))
    for _ in range(number_of_messages):
        await io.send_message(page, message)
