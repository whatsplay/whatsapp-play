__author__ = 'Alexandre Calil Martins Fonseca, github: xandao6'

# region IMPORTS
from wplay.utils.helpers import whatsapp_selectors_dict
from wplay.utils import Logger
from wplay.utils.helpers import logs_path
# endregion


#region LOGGER create
logger : Logger = Logger.setup_logger('logs',logs_path/'logs.log')
#endregion


# region FOR SCRIPTING
def ask_user_for_message():
    logger.info("Input message")
    return str(input("Write your message: "))


def ask_user_for_message_breakline_mode():
    message = []  # type : list[str]
    i = 0
    print("Write your message ('Enter' to breakline)('.' alone to finish):")
    while True:
        message.append(str(input()))
        if message[i] == '.':
            message.pop(i)
            break
        elif message[i] == '...':
            break
        i += 1
    return message


async def send_message(page, message):
    logger.info("Sending message")
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
# endregion
