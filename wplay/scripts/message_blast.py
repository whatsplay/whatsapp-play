# region IMPORTS
from pathlib import Path
from typing import List

from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import target_select
from wplay.utils import io
from wplay.utils.Logger import Logger
from wplay.utils.helpers import logs_path
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


async def message_blast(target: str):
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    if target is not None:
        await target_search.search_and_select_target_all_ways(page, target)  
    else:
        await target_select.manual_select_target(page)
    message : List[str] = io.ask_user_for_message_breakline_mode()
    number_of_messages : int = int(input("Enter the number of messages to blast: "))
    __logger.debug("Blasting messages")
    for _ in range(number_of_messages):
        await io.send_message(page, message)
