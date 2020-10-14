from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from settings import TG_TOKEN, CREDENTIALS_FILE
from sheets import read_range
from bs4 import BeautifulSoup
import requests
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3
from sqlite import *


def end_keyboard():
    end_keyb = ReplyKeyboardMarkup([['Закончить']], resize_keyboard=True)
    return end_keyb


def auth_keyboard():
    contact_button = KeyboardButton('Отправить контакт', request_contact=True)
    auth_keyb = ReplyKeyboardMarkup([[contact_button]], resize_keyboard=True)
    return auth_keyb


def types_keyboard():
    types_keyb = ReplyKeyboardMarkup(get_types(), resize_keyboard=True)
    return types_keyb


def rg_start_keyboard():
    rg_start_keyb = ReplyKeyboardMarkup([['Внести АО на склад', 'Выдать АО'], ['Посмотреть остатки', 'Проверить в МОЗ'], ['Списать АО', 'Вернуть на склад']], resize_keyboard=True)
    return rg_start_keyb