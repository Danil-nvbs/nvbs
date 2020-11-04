import sqlite3
from datetime import datetime, timedelta
from keyboards import *


def get_types():
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM types""")
    types_tuple = cur.fetchall()
    types_list = []
    for elem in types_tuple:
        newelem = list(elem)
        types_list.append(newelem)
    types_list.append(['Закончить'])
    return types_list


def find_type(type):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM types WHERE type= '{type}'")
    type_result = cur.fetchall()
    if type_result == []:
        return 'No'
    else:
        return 'Yes'

def find_si(si):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM users WHERE name= '{si}'")
    type_result = cur.fetchall()
    if type_result == []:
        return 'No'
    else:
        return 'Yes'


def set_command(count, command, id):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    command_number = 'command' + str(count)
    cur.execute(f"UPDATE users SET {command_number} = '{command}' WHERE tgid = '{id}'")
    conn.commit()


def push_phone(name, id):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET tgid = '{id}' WHERE name = '{name}'")
    conn.commit()


def get_si_list(area):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    cur.execute(f"SELECT name FROM users WHERE area = '{area}' AND (role = 'СИ' OR role = 'ВИ')")
    si_tuple = cur.fetchall()
    si_list = []  # Создаём пустой список
    for elem in si_tuple:  # Перебираем список кортежей
        newelem = list(elem)  # Преобразуем кортеж в список
        si_list.append(newelem)  # Добавляем в новый список
    return si_list  # Возвращаем двумерный список


def find_user_by_id(id):
    user_list = users_list()
    result_list = []
    for row in user_list:
        if str(row[2]) == id:
            result_list = row
    return result_list


def add_sn(type, sn, area):
    time_now = datetime.now().strftime('%d.%m.%Y')
    conn = sqlite3.connect('orders.db')  # Коннектимся к ДБ
    cur = conn.cursor()  # Создаём курсор
    db = 'equip_' + area
    cur.execute(f"""INSERT OR REPLACE INTO {db} (type, sn, storage_date) VALUES ('{type}', '{sn}', '{time_now}');""")
    conn.commit()


def users_list():
    conn = sqlite3.connect('orders.db')  # Коннектимся к ДБ
    cur = conn.cursor()  # Создаём курсор
    cur.execute("""SELECT * FROM users;""")  # Отправляем SQL заппрос
    user_tuple = cur.fetchall()  # Получаем ответ
    user_list = []  # Создаём пустой список
    for elem in user_tuple:  # Перебираем список кортежей
        newelem = list(elem)  # Преобразуем кортеж в список
        user_list.append(newelem)  # Добавляем в новый список
    return user_list  # Возвращаем двумерный список


def get_si_remains(area, si):
    conn = sqlite3.connect('orders.db')  # Коннектимся к ДБ
    cur = conn.cursor()  # Создаём курсор
    db = 'equip_' + area
    cur.execute(f"SELECT * FROM {db} WHERE executor = '{si}'")  # Отправляем SQL заппрос
    remains_tuple = cur.fetchall()  # Получаем ответ
    remains_list = []  # Создаём пустой список
    for elem in remains_tuple:  # Перебираем список кортежей
        newelem = list(elem)  # Преобразуем кортеж в список
        remains_list.append(newelem)  # Добавляем в новый список
    finish_text = 'Текущие остатки у исполнителя ' + si + ':\n'
    for elem in remains_list:
        if elem[5] == '' and elem[7] == '':
            finish_text = finish_text + elem[0] + ' - S/N - ' + elem[1] + ' - дата выдачи - ' + elem[2] + ' \n '
    return(finish_text)


def get_area_remains(area):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    db = 'equip_' + area
    cur.execute(f"SELECT * from {db}")
    remains_tuple = cur.fetchall()
    remains_list = []
    for elem in remains_tuple:
        newelem = list(elem)
        remains_list.append(newelem)
    count_store = [0, 0, 0, 0]
    count_si = [0, 0, 0, 0]
    for row in remains_list:
        if row[0] == "Wi-Fi" \
                and (row[3] == "" or row[3] == None) \
                and (row[5] == "" or row[5] == None) \
                and (row[7] == "" or row[7] == None):
            count_store[0] = count_store[0] + 1
        elif row[0] == "TVE" \
                and (row[3] == "" or row[3] == None) \
                and (row[5] == "" or row[5] == None) \
                and (row[7] == "" or row[7] == None):
            count_store[1] = count_store[1] + 1
        elif row[0] == "IPTV" \
                and (row[3] == "" or row[3] == None) \
                and (row[5] == "" or row[5] == None) \
                and (row[7] == "" or row[7] == None):
            count_store[2] = count_store[2] + 1
        elif row[0] == "FiberHome" \
                and (row[3] == "" or row[3] == None) \
                and (row[5] == "" or row[5] == None) \
                and (row[7] == "" or row[7] == None):
            count_store[3] = count_store[3] + 1
        elif row[0] == "Wi-Fi" \
                and (row[3] != "" and row[3] != None) \
                and (row[5] == "" or row[5] == None) \
                and (row[7] == "" or row[7] == None):
            count_si[0] = count_si[0] + 1
        elif row[0] == "TVE" \
                and (row[3] != "" and row[3] != None) \
                and (row[5] == "" or row[5] == None) \
                and (row[7] == "" or row[7] == None):
            count_si[1] = count_si[1] + 1
        elif row[0] == "IPTV" \
                and (row[3] != "" and row[3] != None) \
                and (row[5] == "" or row[5] == None) \
                and (row[7] == "" or row[7] == None):
            count_si[2] = count_si[2] + 1
        elif row[0] == "FiberHome" \
                and (row[3] != "" and row[3] != None) \
                and (row[5] == "" or row[5] == None) \
                and (row[7] == "" or row[7] == None):
            count_si[3] = count_si[3] + 1
    finish_text = f'Остатки в ГКС {area}:\n' \
                  f'На складе:\n' \
                  f'Wi-Fi - {count_store[0]} штук,\n' \
                  f'TVE - {count_store[1]} штук,\n' \
                  f'IPTV - {count_store[2]} штук,\n' \
                  f'FiberHome - {count_store[3]} штук,\n\n' \
                  f'На руках:\n' \
                  f'Wi-Fi - {count_si[0]} штук,\n' \
                  f'TVE - {count_si[1]} штук,\n' \
                  f'IPTV - {count_si[2]} штук,\n' \
                  f'FiberHome - {count_si[3]} штук.'
    return finish_text

def take_to_si(area, si, sn, bot, update):
    time_now = datetime.now().strftime('%d.%m.%Y')
    conn = sqlite3.connect('orders.db')  # Коннектимся к ДБ
    cur = conn.cursor()  # Создаём курсор
    db = 'equip_' + area
    cur.execute(f"SELECT type, executor FROM {db} WHERE sn = '{sn}'")
    result = cur.fetchall()
    if len(result) == 0:
        cur.execute(f"INSERT OR REPLACE INTO {db} (type, sn, storage_date, executor, take_date) VALUES ('Неизвестно', '{sn}', '{time_now}', '{si}', '{time_now}')")
        conn.commit()
        bot.message.reply_text(f'Оборудование {sn} добавлено на склад {area} и выдано СИ {si}.\nВнесите ещё серийный номер или выберите действиие')
        return('added')
    elif len(result[0]) == 1:
        cur.execute(f"UPDATE {db} SET executor = '{si}', take_date = '{time_now}' WHERE sn = '{sn}'")
        conn.commit()
        bot.message.reply_text(f'Оборудование {sn} выдано СИ {si}.\nВнесите ещё серийный номер или выберите действиие')
        return('taked')
    elif len(result[0]) == 2:
        cur.execute(f"UPDATE {db} SET executor = '{si}', take_date = '{time_now}' WHERE sn = '{sn}'")
        conn.commit()
        bot.message.reply_text(f'Оборудование {sn} перевыдано СИ {si}.\nВнесите ещё серийный номер или выберите действиие')
        return('re-taked')





"""
conn = sqlite3.connect('orders.db')  # Коннектимся к ДБ
cur = conn.cursor()  # Создаём курсор
cur.execute("CREATE TABLE IF NOT EXISTS equip_4_5 (type TEXT,
    sn TEXT PRIMARY KEY,
    storage_date TEXT,
    executor TEXT,
    take_date TEXT,
    cont_moz TEXT,
    cont_moz_date TEXT,
    cont_ex TEXT,
    cont_ex_date TEXT);
")
conn.commit()

 cur.execute("INSERT INTO users(name, phone, tgid, role, area)
   VALUES('Осипов Данил Дмитриевич', '79636871080', '373531147', 'РГ', '4_6');")
 conn.commit()

 cur.execute("INSERT OR REPLACE INTO types(type) VALUES('Cable 305m');")
 conn.commit()
 cur.execute("SELECT * FROM types;")
 one_result = cur.fetchall()
 print(one_result)
 """