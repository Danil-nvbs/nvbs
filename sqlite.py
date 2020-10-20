import sqlite3
from datetime import datetime, timedelta


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
    count = 0
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
    print(remains_list)
    return(remains_list)


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