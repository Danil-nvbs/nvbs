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
from sqlite import *
from keyboards import *


def auth(bot, update):
    ulist = users_list()
    user_name = None
    phone_number = bot.message.contact.phone_number[1:]
    if phone_number[0] != '7':
        phone_number = '7' + phone_number
    for row in ulist:
        if row[1] == phone_number:
            user_name = row[0]
            push_phone(row[0], bot.message.chat.id)
    if user_name != None:
        start_menu(bot, update)
    else:
        bot.message.reply_text('Номер телефона не найден, обратитесь к руководителю.', reply_markup=auth_keyboard())


def start_menu(bot, update):
    user_list = users_list()
    user_name = None
    for row in user_list:
        if row[2] == bot.message.chat.id:
            user_name = row[0]
            user_phone = row[1]
            user_role = row[3]
            user_area = row[4]
            user_com1 = row[5]
            user_com2 = row[6]
            user_com3 = row[7]
            user_com4 = row[8]
    set_command(1, "Начало", bot.message.chat.id)
    set_command(2, '', bot.message.chat.id)
    set_command(3, '', bot.message.chat.id)
    set_command(4, '', bot.message.chat.id)
    if user_name == None:
        bot.message.reply_text(f'Необходимо пройти авторизацию', reply_markup=auth_keyboard())
    else:
        bot.message.reply_text(f'Привет {user_name}, роль - {user_role}, телефон {user_phone}', reply_markup=rg_start_keyboard())



def store_add_equip(bot, update):
    bot.message.reply_text('Выберите тип оборудования', reply_markup=types_keyboard())
    set_command('1', "Внести АО", bot.message.chat.id)

def big_handler(bot, update):
    row = find_user_by_id(str(bot.message.chat.id))
    user_name = row[0]
    user_phone = row[1]
    user_role = row[3]
    user_area = row[4]
    user_com1 = row[5]
    user_com2 = row[6]
    user_com3 = row[7]
    user_com4 = row[8]
    if (user_com1 == "Внести АО") and (find_type(bot.message.text) == 'Yes') and (user_com2 == '') and (user_role == 'РГ' or user_role == "ВИ"):
        set_command(2, bot.message.text, bot.message.chat.id)
        bot.message.reply_text('Введите серийные номера в поле ввода \nНажмите "Сменить тип" для внесения '
                               'оборудования другого типа \nНажмите "Закончить" после ввода',
                               reply_markup=end_change_type_keyboard())
    if (user_com1 == "Внести АО") and (find_type(user_com2) == "Yes") and (user_role == 'РГ' or user_role == 'ВИ') and bot.message.text != "Закончить" and bot.message.text != "Сменить тип":
        layout = dict(zip(map(ord, "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                                   'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
                                   "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                                   "QWERTYUIOP{}ASDFGHJKL:'ZXCVBNM<>?~"))
        add_sn(user_com2, bot.message.text.translate(layout).upper(), user_area)
        bot.message.reply_text(f'Оборудование с серийным номером {bot.message.text.translate(layout).upper()} внесено на склад. Введите ещё '
                               f'серийник или нажмите "Закончить"')
    if (user_com1 == "Внести АО") and (find_type(user_com2) == "Yes") and (user_role == 'РГ' or user_role == 'ВИ') and bot.message.text == "Сменить тип":
        set_command(2, '', bot.message.chat.id)
        store_add_equip(bot, update)


def chose_type(bot, update):
    bot.message.reply_text('Выберирири', reply_markup=end_keyboard())
    return "SN"


def get_anecdote(bot, update):
    recive = requests.get('http://anekdotme.ru/random')
    page = BeautifulSoup(recive.text, "html.parser")
    find = page.select('.anekdot_text')
    for text in find:
        page = (text.getText().strip())
    bot.message.reply_text(page)