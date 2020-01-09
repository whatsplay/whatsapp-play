import os
import tkinter
from tkinter import filedialog
from pathlib import Path
from telegram import Message, Update
from telegram.ext import CommandHandler, Updater, Filters


def start_tkinter():
    root_window = tkinter.Tk()
    root_window.withdraw()


def ask_where_are_the_status_file():
    print('Choose a status text file.')
    status_file_path = filedialog.askopenfile(
        title='Choose a status text file.',
        filetypes=['TXT files', ('.txt', '.xml')]
    )
    if status_file_path == ():
        print("Error! Choose a status.")
        exit()
    return status_file_path


def get_filename_from_path(path):
    parts_from_path = Path(path).parts
    filename_with_extension = os.path.splitext(parts_from_path[-1])
    return filename_with_extension


def startmessage(bot , update):
    chat_id = update.message.chat_id
    text = '''
        Hi, I am here to send all the messages you want to track online status in whatsapp :)
    '''
    bot.send_message(chat_id = chat_id , text = text)


def send_status(bot, update, filename_with_extension):
    # Display last updated online status message
    chat_id = update.message.chat_id
    try:
        f=open(os.path.join('tracking_data' , filename_with_extension[0]),'r')
        file_data = f.readlines()
        text = file_data[len(file_data) - 1]
        bot.send_message(chat_id = chat_id , text = text)
    except:
        bot.send_message(chat_id = chat_id , text = 'oops! An error occurred')


def telegram_status(name):
    print(name)

    start_tkinter()
    file_path = ask_where_are_the_status_file()
    filename_with_extension = get_filename_from_path(file_path)
    
    #add bot token
    global TOKEN
    TOKEN = input("enter token: ")
    # Added all the essential command handlers 
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start' ,startmessage))
    dp.add_handler(CommandHandler('status' ,send_status))
    updater.start_polling()
    updater.idle()
