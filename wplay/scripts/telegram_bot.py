import tkinter
from tkinter import filedialog
from telegram.ext import CommandHandler, Updater
from wplay.utils.helpers import data_folder_path

status_file_path = None


def start_tkinter():
    root_window = tkinter.Tk()
    root_window.withdraw()


def ask_where_are_the_status_file():
    print('Choose a status text file.')
    status_file_path = filedialog.askopenfile(
        initialdir = data_folder_path / 'tracking_data',
        title = 'Choose a status text file.',
        filetypes = (("text files", "*.txt"), ("all files", "*.*"))
    )
    if status_file_path == ():
        print("Error! Choose a status.")
        exit()
    return status_file_path


def startmessage(bot, update):
    chat_id : int = update.message.chat_id
    text : str = '''
        Hi, I am here to send all the messages you want to track online status in whatsapp :)
    '''
    bot.send_message(chat_id = chat_id, text = text)


def send_status(bot, update):
    # Display last updated online status message
    chat_id = update.message.chat_id
    try:
        f = open(status_file_path, 'r')
        file_data = f.readlines()
        text : Union[str , bytes] = file_data[len(file_data) - 1]
        bot.send_message(chat_id = chat_id, text = text)
    except:
        bot.send_message(chat_id = chat_id, text = 'oops! An error occurred')


def telegram_status(name):
    print(name)
    start_tkinter()
    global status_file_path
    status_file_path = ask_where_are_the_status_file()
    # Add bot token
    global TOKEN
    TOKEN = input("enter token: ")
    # Added all the essential command handlers
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', startmessage))
    dp.add_handler(CommandHandler('status', send_status))
    updater.start_polling()
    updater.idle()
