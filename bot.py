from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from settings import TG_TOKEN, CREDENTIALS_FILE
from sheets import read_range
from bs4 import BeautifulSoup
import requests
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3


# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API





def sms2(bot, update):
    bot.message.reply_text('Введите количество подключений, {}'.format(bot.message.chat.id))
    my_keyboard = ReplyKeyboardMarkup([['/start', 'Анекдот', '2'], ['3', '4', '5', '6']], resize_keyboard=True)
    bot.message.reply_text('Hello {}'
                           .format(bot.message.chat.id), reply_markup=get_keyboard())
    print(bot.message)

def read(bot, update):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS equip(
       type TEXT,
       sn TEXT PRIMARY KEY,
       storage_date TEXT,
       executor TEXT,
       take_date TEXT,
       cont_moz TEXT,
       cont_moz_date TEXT,
       cont_ex TEXT,
       cont_ex_date TEXT);
    """)
    conn.commit()
    print('read_')
#    print(read_range('1iR0aBHAc4iWvUWxS5_R1zxr7StyL8zPe7YTVKhohLlY', '4_6!B2:B'))
    res = read_range('1iR0aBHAc4iWvUWxS5_R1zxr7StyL8zPe7YTVKhohLlY', '4_6!A2:I')
    real_result = []
    for line in res:
        one_line = []
        for cell in line:
            if cell == None:
                cell = ' '
            print(cell)
            one_line.append(cell)
        t = tuple(one_line)

        cur.execute('INSERT INTO equip VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (t))
        cur.execute("SELECT * FROM equip;")
        three_results = cur.fetchall()
        print(three_results)


def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([['Анекдот'], ['Начать'], ['Читать']], resize_keyboard=True)
    return my_keyboard


def get_anecdote(bot, update):
    recive = requests.get('http://anekdotme.ru/random')
    page = BeautifulSoup(recive.text, "html.parser")
    find = page.select('.anekdot_text')
    for text in find:
        page = (text.getText().strip())
    bot.message.reply_text(page)


def parrot(bot, update):
    print(bot.message.text)
    bot.message.reply_text(bot.message.text)


def sms(bot, update):
    print('Кто-то отправил /start, что делать?')
    bot.message.reply_text('Здравствуйте, я бот')


def main():
    my_bot = Updater(TG_TOKEN)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote))
    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    my_bot.dispatcher.add_handler(CommandHandler('h1', sms2))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Читать'), read))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()
    my_bot.idle()


main()
