from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler
from telegram.ext import Filters
from settings import TG_TOKEN

def sms2(bot, update):
    bot.message.reply_text('Введите количество подключений, {}'.format(bot.message.chat.id))
    print(bot.message)

def parrot(bot, update):
    print(bot.message.text)
    bot.message.reply_text(bot.message.text)

def sms(bot, update):
    print('Кто-то отправил /start, что делать?')
    bot.message.reply_text('Здравствуйте, я бот')

def main():
    my_bot = Updater(TG_TOKEN)
    my_bot.dispatcher.add_handler(CommandHandler('start', sms))
    my_bot.dispatcher.add_handler(MessageHandler(Filters.text, parrot))
    my_bot.dispatcher.add_handler(CommandHandler('h1', sms2))
    my_bot.start_polling()
    my_bot.idle()

main()