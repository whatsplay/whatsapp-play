# region IMPORTS
from pathlib import Path

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


async def chat(target):
    __logger.info("Chatting with target")
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

    print("\033[91m {}\033[00m".format("\nType '...' in a new line or alone in the message to change target person.\nType '#_FILE' to send Image/Video/Documentd etc.\n"))

    while True:
        message : list[str] = io.ask_user_for_message_breakline_mode()

        if '...' in message:
            message.remove('...')
            await io.send_message(page, message)
            target = input("\n\nNew Target Name: ")
            if target is not None:
                await target_search.search_and_select_target(page, target)
            else:
                await target_select.manual_select_target(page)
            message = io.ask_user_for_message_breakline_mode()

        #File Share:
        if '#_FILE' in message:
            message.remove('#_FILE')
            await io.send_file(page)

        await io.send_message(page, message)
