from wplay.utils import browser_config
from wplay.utils import target_search
from wplay.utils import target_select
from wplay.utils import io
from wplay.utils import Logger
from wplay.utils.helpers import logs_path


#region LOGGER create
logger = Logger.setup_logger('logs',logs_path/'logs.log')
#endregion


async def blast(target):
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    if target is not None:
        try:
            await target_search.search_and_select_target(page, target)
        except Exception as e:
            print(e)
            await target_search.search_and_select_target_without_new_chat_button(page,target)
    else:
        await target_select.manual_select_target(page)
    message : list[str] = io.ask_user_for_message_breakline_mode()
    number_of_messages : int = int(input("Enter the number of messages to blast: "))
    for _ in range(number_of_messages):
        logger.info("Blasting messages")
        await io.send_message(page, message)
