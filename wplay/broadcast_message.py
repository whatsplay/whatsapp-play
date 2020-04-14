# region IMPORTS
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
# endregion

# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion

class InvalidNumber(Exception):
    message = "Either Number is invalid or no account exist for the number or the number was kept in wrong format :(\n"


def ProcessNumbers():
    __logger.info("Processing numbers.")
    print("Choose a text file containing full numbers with country code, one number per line.")
    Tk().withdraw()
    filename = askopenfile(
        initialdir = data_folder_path,
        title = 'Choose a text file with numbers.',
        filetypes = [("text files", "*.txt")],
        mode="r"
    )
    numbers = filename.readlines()
    for i in range(len(numbers)):
        number = numbers[i].strip("\n+")
        numbers[i]=number
    return numbers


async def broadcast():
    __logger.info("Broadcast message.")
    FailureReport = list()
    page, _ = await browser_config.configure_browser_and_load_whatsapp()
    numbers = ProcessNumbers()
    message : List[str] = io.ask_user_for_message_breakline_mode()

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

    if FailureReport != []:
        for i,r in enumerate(FailureReport):
            print(i,r)
        for r in report:
            __logger.error(r)
    else:
        __logger.info("Messages broadcasted successfully!")
        print("Messages broadcasted successfully!")
