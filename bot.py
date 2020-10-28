from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from settings import TG_TOKEN, CREDENTIALS_FILE
from sheets import read_range
from bs4 import BeautifulSoup
import requests
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3
from datetime import datetime, timedelta
from keyboards import *
from handlers import *
from sheets import *
from sqlite import *

TG_TOKEN = "1209301262:AAHFpm5MiDbvARPdb9rcO6jYnFBCVB3u6sI"
CREDENTIALS_FILE = 'pyconnect-292200-4e5bbf9ac5ff.json'







def main():
    my_bot = Updater(TG_TOKEN)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Внести АО на склад'), store_add_equip))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, auth))
    my_bot.dispatcher.add_handler(CommandHandler('start', start_menu))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Закончить'), start_menu))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, big_handler))
    my_bot.start_polling()
    my_bot.idle()


if __name__ == '__main__':
    main()