# region IMPORTS
import tkinter
from tkinter import filedialog
from pathlib import Path
import pickle

from telegram.ext import CommandHandler, Updater
from wplay.utils.helpers import data_folder_path
from wplay.utils.Logger import Logger
# endregion


# region LOGGER
__logger = Logger(Path(__file__).name)
# endregion


status_file_path = None


def start_tkinter():
    root_window = tkinter.Tk()
    root_window.withdraw()


def ask_where_are_the_status_file():
    print('Choose a status text file.')
    status_file_path = filedialog.askopenfile(
        initialdir=data_folder_path / 'tracking_data',
        title='Choose a status text file.',
        filetypes=(("text files", "*.txt"), ("all files", "*.*"))
    )
    if status_file_path == ():
        print("Error! Choose a status.")
        exit()
    return status_file_path


def startmessage(bot, update):
    chat_id: int = update.message.chat_id
    text: str = '''
        Hi, I am here to send all tracked online status in whatsapp :)
    '''
    bot.send_message(chat_id=chat_id, text=text)


def send_status(bot, update):
    # Display last updated online status message
    chat_id = update.message.chat_id
    try:
        f = open(status_file_path, 'r')
        file_data = f.readlines()
        text: Union[str, bytes] = file_data[len(file_data) - 1]
        bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=chat_id, text='oops! An error occurred')


def telegram_status(name):
    print(name)
    start_tkinter()
    global status_file_path
    status_file_path = ask_where_are_the_status_file()
    # Add bot token
    global TOKEN
    new_token = False
    token_file_path = "wplay/telegram_token.pkl"
    if Path(token_file_path).exists():
        user_choice = input("Do you want to use last saved token (Y) or enter new token (N): ")
        if user_choice in "Yy":
            with open(token_file_path, "rb") as token_file:
                TOKEN = pickle.load(token_file)
        else:
            new_token = True
    else:
        new_token = True
    if new_token:
        TOKEN = input("Enter token: ")
        with open(token_file_path, "wb") as token_file:
            pickle.dump(TOKEN, token_file)

    # Added all the essential command handlers
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', startmessage))
    dp.add_handler(CommandHandler('status', send_status))
    updater.start_polling()
    updater.idle()
