from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from settings import TG_TOKEN, CREDENTIALS_FILE
from bs4 import BeautifulSoup
import requests
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API
driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API



def read_range(spreadsheetId, range):

    results = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId,
                                                   ranges=range,
                                                   valueRenderOption='FORMATTED_VALUE',
                                                   dateTimeRenderOption='FORMATTED_STRING').execute()
    sheet_values = results['valueRanges'][0]['values']
    return sheet_values