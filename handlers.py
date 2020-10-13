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


def start_menu(bot, update):
    ulist = users_list()
 #   for row in ulist:
 #       if row[2] ==



def store_add_equip(bot, update):
    bot.message.reply_text('Выберите тип оборудования', reply_markup=types_keyboard())
    return "Выбери"

def chose_type(bot, update):
    bot.message.reply_text('Выберирири', reply_markup=end_keyboard())
    return "SN"


def sms2(bot, update):
    bot.message.reply_text('Введите количество подключений, {}'.format(bot.message.chat.id))
    my_keyboard = ReplyKeyboardMarkup([['/start', 'Анекдот', '2'], ['3', '4', '5', '6']], resize_keyboard=True)
    bot.message.reply_text('Hello {}'
                           .format(bot.message.chat.id), reply_markup=get_keyboard())
    print(bot.message)

def get_anecdote(bot, update):
    recive = requests.get('http://anekdotme.ru/random')
    page = BeautifulSoup(recive.text, "html.parser")
    find = page.select('.anekdot_text')
    for text in find:
        page = (text.getText().strip())
    bot.message.reply_text(page)


def sms(bot, update):
    print('Кто-то отправил /start, что делать?')
    bot.message.reply_text('Здравствуйте, я бот')