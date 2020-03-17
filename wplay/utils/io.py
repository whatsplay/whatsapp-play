__author__ = 'Alexandre Calil Martins Fonseca, github: xandao6'

# region IMPORTS
from wplay.utils.helpers import whatsapp_selectors_dict
# endregion


# region FOR SCRIPTING
def ask_user_for_message():
    return str(input("Write your message: "))


def ask_user_for_message_breakline_mode():
    message = []
    i = 0
    print("Write your message ('Enter' to breakline)('.' alone to finish):")
    while True:
        message.append(str(input()))
        if message[i] == '.':
            message.pop(i)
            break
        i += 1
    return message


async def send_message(page, message):
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
