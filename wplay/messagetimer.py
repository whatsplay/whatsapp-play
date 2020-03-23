import time
import random

from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import target_select
from wplay.utils import io
from wplay.utils import Logger
from wplay.utils.helpers import logs_path


#region LOGGER create
logger = Logger.setup_logger('logs',logs_path/'logs.log')
#endregion


async def msgTimer(target):
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    if target is not None:
        try:
            await target_search.search_and_select_target(page, target)
        except Exception as e:
            print(e)
            await page.reload()
            await target_search.search_and_select_target_without_new_chat_button(page, target)
    else:
        await target_select.manual_select_target(page)
    # Region INPUTS
    logger.info("Input message information for message timer")
    message_type_numbers : int = int(
        input("How many types of messages will you send? "))
    messages : list[str] = list()
    for _ in range(message_type_numbers):
        messages.append(io.ask_user_for_message_breakline_mode())
    number_of_messages : int = int(input("Enter the number of messages to send: "))
    minimumTimeInterval : int = int(
        input("Enter minimum interval number in seconds: "))
    maximumTimeInterval : int = int(
        input("Enter maximum interval number in seconds: "))
    # Endregion

    random.seed()
    for _ in range(number_of_messages):
        if not messages:
            break
        await io.send_message(page, messages[random.randrange(0, message_type_numbers)])
        if minimumTimeInterval != maximumTimeInterval:
            time.sleep(random.randrange(minimumTimeInterval, maximumTimeInterval))
        else:
            time.sleep(minimumTimeInterval)
