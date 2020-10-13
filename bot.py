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
from keyboards import *
from handlers import *
from sheets import *



def test():
    name = 'Огдаров Хасан Бобокулович'
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    print('Поехали')
    cur.execute(f"select * FROM equip_4_6 where executor='{name}'")
    new_result = cur.fetchall()
    print(new_result)
    print(len(new_result))


def read(bot, update):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    print('read_')
    res =read_range('1iR0aBHAc4iWvUWxS5_R1zxr7StyL8zPe7YTVKhohLlY', 'Data!A2:I')
#    res = read_range('1iR0aBHAc4iWvUWxS5_R1zxr7StyL8zPe7YTVKhohLlY', '4_6!A2:I')
    real_result = []
    for line in res:
        one_line = []
        for cell in line:
            if cell == None:
                cell = ' '
            one_line.append(cell)
        while len(one_line) < 9:
            one_line.append('')
        t = tuple(one_line)
        real_result.append(t)
    cur.executemany("INSERT OR REPLACE INTO users VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?);", real_result)
#    cur.execute('INSERT OR REPLACE INTO equip VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (t))
    conn.commit()
#        cur.execute("SELECT * FROM equip;")
#        three_results = cur.fetchall()
#        print(three_results)
#    query = 'Тихонов Дмитрий Васильевич'
    cur.execute("select * FROM users")
    new_result = cur.fetchall()
    print(new_result)
    print(len(new_result))
#    new_result = cur.fetchall()
#    print(new_result)
#    print(len(new_result))
#    for element in new_result:
#        element[2]
 #   bot.message.reply_text(new_result[1])


def main():
    my_bot = Updater(TG_TOKEN)
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Анекдот'), get_anecdote))
    my_bot.dispatcher.add_handler(CommandHandler('start', start_menu))
    my_bot.dispatcher.add_handler(CommandHandler('h1', sms2))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, read))
    my_bot.start_polling()
    my_bot.idle()


if __name__ == '__main__':
    main()