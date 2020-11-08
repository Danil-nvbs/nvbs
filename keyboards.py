from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from settings import TG_TOKEN, CREDENTIALS_FILE
from bs4 import BeautifulSoup
import requests
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import sqlite3
from sqlite import *


def end_change_type_keyboard():
    end_change_type_keyb = ReplyKeyboardMarkup([['Сменить тип'], ['Закончить']], resize_keyboard=True)
    return end_change_type_keyb


def end_change_si_keyboard():
    end_change_si_keyb = ReplyKeyboardMarkup([['Сменить получателя'], ['Закончить']], resize_keyboard=True)
    return end_change_si_keyb


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


def start_keyboard(role):
    if role == 'РГ':
        start_keyb = ReplyKeyboardMarkup(
            [['Внести АО на склад', 'Выдать АО'],
             ['Посмотреть остатки', 'Проверить в МОЗ'],
             ['Списать АО', 'Вернуть на склад']],
            resize_keyboard=True)
    elif role == 'ВИ':
        start_keyb = ReplyKeyboardMarkup(
            [['Внести АО на склад', 'Выдать АО'],
             ['Свои остатки', 'Общие остатки'],
             ['Списать своё АО', 'Списать чужое АО'],
             ['Проверить в МОЗ','Вернуть на склад']],
            resize_keyboard=True)
    elif role == 'СИ':
        start_keyb = ReplyKeyboardMarkup(
            [['Посмотреть свои остатки', 'Списать на заявки'],
             ['Передать оборудование', 'Вернуть на склад']],
            resize_keyboard=True)
    elif role == 'ДМР':
        start_keyb = ReplyKeyboardMarkup(
            [['Остатки по группам']],
            resize_keyboard=True)
    return start_keyb


def make_si_keyboard(area):
    si_list = get_si_list(area)
    new_list = []
    count = 2
    print('123')
    for elem in si_list:
        if (count % 2) == 0:
            new_list.append(elem)
        if (count % 2) != 0:
            new_list[len(new_list) - 1].append(elem[0])
        count = count + 1
    new_list.append(['Закончить'])
    si_keyboard = ReplyKeyboardMarkup(new_list,resize_keyboard=True)
    return si_keyboard




