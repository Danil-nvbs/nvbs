from handlers import *
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from bs4 import BeautifulSoup
from settings import TG_TOKEN
import requests

from sheets import *

# heroku ps:scale worker=1
# heroku logs --tail


def main():
    print('Начали')
    my_bot = Updater(TG_TOKEN)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.contact, auth))
    my_bot.dispatcher.add_handler(CommandHandler('start', start_menu))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Закончить'), start_menu))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, big_handler))
    my_bot.start_polling()
    my_bot.idle()


if __name__ == "__main__":
    main()
