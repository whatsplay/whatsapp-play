# region IMPORTS
from pathlib import Path
from typing import List, Union

from pyppeteer.page import Page

from wplay.utils.helpers import whatsapp_selectors_dict
from wplay.utils.Logger import Logger
from wplay.utils.helpers import logs_path
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


# region FOR SCRIPTING
def ask_user_for_message() -> str:
    return str(input("Write your message: "))


def ask_user_for_message_breakline_mode() -> List[str]:
    message = list()
    i = 0
    print("Write your message (Enter key to breakline)('.' alone to send):")
    while True:
        message.append(str(input()))
        if message[i] == '.':
            message.pop(i)
            break
        elif message[i] == '...' or message[i] == '#_FILE':
            break
        i += 1
    return message


async def send_message(page: Page, message: Union[List[str], str]):
    __logger.debug("Sending message")
    for i in range(len(message)):
        await page.type(
            whatsapp_selectors_dict['message_area'],
            message[i]
        )
        if isinstance(message, list):
            await page.keyboard.down('Shift')
            await page.keyboard.press('Enter')
            await page.keyboard.up('Shift')
    await page.keyboard.press('Enter')


async def send_file(page):
    __logger.info("Sending File")
    await page.click(whatsapp_selectors_dict['attach_file'])
    await page.click(whatsapp_selectors_dict['choose_file'])
    await page.waitForSelector(whatsapp_selectors_dict['send_file'],timeout=30000)
    await page.click(whatsapp_selectors_dict['send_file'])
# endregion
