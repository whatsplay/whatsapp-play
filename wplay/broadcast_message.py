#Region IMPORTS
from tkinter import Tk
from tkinter.filedialog import askopenfile
from pathlib import Path

from wplay.utils import browser_config
from wplay.utils.target_search import search_and_select_target as find_target
from wplay.utils.target_search import __try_load_contact_by_number as number_valid
from wplay.utils import io
from typing import List
from wplay.utils.helpers import data_folder_path
from wplay.utils.Logger import Logger
#End Region

# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion

class InvalidNumber(Exception):
    message = "Either Number is invalid or no account exist for the number or the number was kept in wrong format :(\n"


def ProcessNumbers():
    Tk().withdraw()
    filename = askopenfile(
        initialdir = data_folder_path / 'tracking_data',
        title = 'Choose a text file containing the number.',
        filetypes = [("text files", "*.txt")],
        mode="r"
    )
    numbers = filename.readlines()
    for i,number in enumerate(numbers):
        number = number.strip("\n+")
        if len(number)==10 :
            number = "91"+number
        numbers[i]=number
    return numbers

def GetMessage() -> List[str]:
    message = list()
    i = 0
    print("Write your message (Enter key to breakline)('.' alone to complete your message):")
    while True:
        message.append(str(input()))
        if message[i] == '.':
            message.pop(i)
            break
        i += 1
    return message


async def broadcast():
    __logger.info("Broadcast message.")
    numbers = ProcessNumbers()
    message : list[str] = GetMessage()
    FailureReport = []
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    for number in numbers:
        try :
            if not await number_valid(page,number):
                raise InvalidNumber
            await find_target(page, number)
        except InvalidNumber as e:
            report = number + "\t" + e.message + "\n"
            FailureReport.append(report)
            continue
        await io.send_message(page,message)
    if FailureReport != [] :
        for i,r in enumerate(FailureReport):
            print(i,r)
    else:
        print("Mesaage is broadcasted to all number succesfully :) \n")
