from telegram import Message, Update, Bot, User
from telegram.ext import CommandHandler , Updater , MessageHandler , Filters , run_async
import os

'''
#Bot token goes here
TOKEN = input("enter telegram token: ")
'''

def send_status(bot, update):
	# Display last updated online status message
	chat_id = update.message.chat_id
	try:
		text = 'online'
		bot.send_message(chat_id = chat_id , text = text)
	except:
		bot.send_message(chat_id = chat_id , text = 'oops! An error occurred')


def tgmessage(tgtoken):
	# Added all the essential command handlers 
	TOKEN = tgtoken
	updater = Updater(TOKEN)
	dp = updater.dispatcher
	dp.add_handler(CommandHandler('status' ,send_status))
	updater.start_polling()
	updater.idle()
