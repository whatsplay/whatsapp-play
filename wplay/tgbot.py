from telegram import Message, Update
from telegram.ext import CommandHandler, Updater, Filters
import os

def startmessage(bot , update):
	chat_id = update.message.chat_id
	text = '''
		Hi, I am here to send all the messages you want to track online status in whatsapp :)
	'''
	bot.send_message(chat_id = chat_id , text = text)

def send_status(bot, update):
	# Display last updated online status message
	chat_id = update.message.chat_id
	try:
		f=open(os.path.join('online_status_data' , 'status.txt'),'r')
		file_data = f.readlines()
		text = file_data[len(file_data) - 1]
		bot.send_message(chat_id = chat_id , text = text)
	except:
		bot.send_message(chat_id = chat_id , text = 'oops! An error occurred')


def telegram_status(name):
	print(name)
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
