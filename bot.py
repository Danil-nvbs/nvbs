from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from settings import TG_TOKEN
from bs4 import BeautifulSoup
import requests
def sms2(bot, update):
    bot.message.reply_text('Введите количество подключений, {}'.format(bot.message.chat.id))
    my_keyboard = ReplyKeyboardMarkup([['/start', 'Анекдот','2'],['3','4','5','6']])
    bot.message.reply_text('Hello {}'
                           .format(bot.message.chat.id), reply_markup=my_keyboard)
    print(bot.message)

def get_anecdote(bot, update):
    recive = requests.get('http://anekdotme.ru/random')
    print(recive.text)
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
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()
    my_bot.idle()

main()