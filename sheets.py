from sqlite import *
from oauth2client.service_account import ServiceAccountCredentials
from settings import CREDENTIALS_FILE
import httplib2
import apiclient.discovery


def read_range(spreadsheetId, range):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API
    driveService = apiclient.discovery.build('drive', 'v3',
                                             http=httpAuth)  # Выбираем работу с Google Drive и 3 версию API
    results = service.spreadsheets().values().batchGet(spreadsheetId=spreadsheetId,
                                                       ranges=range,
                                                       valueRenderOption='FORMATTED_VALUE',
                                                       dateTimeRenderOption='FORMATTED_STRING').execute()
    sheet_values = results['valueRanges'][0]['values']
    return sheet_values


def set_range(spreadsheetId, range, values):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                   ['https://www.googleapis.com/auth/spreadsheets',
                                                                    'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе

    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API
    driveService = apiclient.discovery.build('drive', 'v3',
                                             http=httpAuth)  # Выбираем работу с Google Drive и 3 версию API

    results = service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId,
                                                          body={
                                                              "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
                                                              "data": [{"range": range,
                                                                        "majorDimension": "ROWS", # Сначала заполнять строки, затем столбцы
                                                                        "values": values}]
                                                              }
                                                          ).execute()

def moz_check(area):
    wifi_sn_list = read_range('1C93At0VJH5I2ZCjrAQtmJnSrF-8dUECE1RKetRXcSbk', 'БМОЛ!D2:D')
    wifi_cont_list = read_range('1C93At0VJH5I2ZCjrAQtmJnSrF-8dUECE1RKetRXcSbk', 'БМОЛ!F2:F')
    alt_sn = read_range('1C93At0VJH5I2ZCjrAQtmJnSrF-8dUECE1RKetRXcSbk', 'moz2!B2:B')
    for elem in alt_sn:
        wifi_sn_list.append(elem)
    alt_cont = read_range('1C93At0VJH5I2ZCjrAQtmJnSrF-8dUECE1RKetRXcSbk', 'moz2!D2:D')
    for elem in alt_cont:
        wifi_cont_list.append(elem)
    alt2_sn = read_range('1qSjLhAgkvdkABJcn0F-jdbmMTS9vpje9Wc31kGxWYGs', 'бмол!D2:D')
    for elem in alt2_sn:
        wifi_sn_list.append(elem)
    alt2_cont = read_range('1qSjLhAgkvdkABJcn0F-jdbmMTS9vpje9Wc31kGxWYGs', 'бмол!F2:F')
    for elem in alt2_cont:
        wifi_cont_list.append(elem)
    alt3_sn = read_range('1qSjLhAgkvdkABJcn0F-jdbmMTS9vpje9Wc31kGxWYGs', 'moz!B2:B')
    for elem in alt3_sn:
        wifi_sn_list.append(elem)
    alt3_cont = read_range('1qSjLhAgkvdkABJcn0F-jdbmMTS9vpje9Wc31kGxWYGs', 'moz!B2:B')
    for elem in alt3_cont:
        wifi_cont_list.append(elem)
    remains_list = get_remains_wifi_moz(area)
    count = 0
    for elem in remains_list:
        i = 0
        while i < len(wifi_sn_list):
            if wifi_sn_list[i][0] == elem[0] and wifi_cont_list[i][0] != "0":
                set_sn_cont(area, elem[0], wifi_cont_list[i][0])
                count = count + 1
            i = i + 1
    return count
