from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from settings import TG_TOKEN
from bs4 import BeautifulSoup
import requests
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
CREDENTIALS_FILE = 'pyconnect-292200-4e5bbf9ac5ff.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
spreadsheetId = '10JZZnmHUXdC0sMdn4lBZ6RZmElCmGzAHWvtWzsp9ti4' # сохраняем идентификатор файла
ranges = ["Еще один лист!A2:F8"]  #

results = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId,
                                                   ranges=ranges,
                                                   valueRenderOption='FORMATTED_VALUE',
                                                   dateTimeRenderOption='FORMATTED_STRING').execute()
sheet_values = results['valueRanges'][0]['values']
print(sheet_values)

def sms2(bot, update):
    bot.message.reply_text('Введите количество подключений, {}'.format(bot.message.chat.id))
    my_keyboard = ReplyKeyboardMarkup([['/start', 'Анекдот', '2'], ['3', '4', '5', '6']], resize_keyboard=True)
    bot.message.reply_text('Hello {}'
                           .format(bot.message.chat.id), reply_markup=get_keyboard())
    print(bot.message)

def read(bot, update):
    bot.message.reply_text(sheet_values)

def get_keyboard():
    my_keyboard = ReplyKeyboardMarkup([['Анекдот'], ['Начать'], ['Читать']], resize_keyboard=True)
    return my_keyboard


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
    my_bot.dispatcher.add_handler(MessageHandler(Filters.regex('Читать'), read))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.start_polling()
    my_bot.idle()


main()
