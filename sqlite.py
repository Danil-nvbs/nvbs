import sqlite3

def get_types():
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM types""")
    types_tuple = cur.fetchall()
    types_list = []
    for elem in types_tuple:
        newelem = list(elem)
        types_list.append(newelem)
    return types_list


def set_command(count,command, id):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    command_number = 'command' + count
    cur.execute(f"UPDATE users SET {command_number} = '{command}' WHERE tgid = '{id}'")
    conn.commit()

def push_phone(name, id):
    conn = sqlite3.connect('orders.db')
    cur = conn.cursor()
    cur.execute(f"UPDATE users SET tgid = '{id}' WHERE name = '{name}'")
    conn.commit()


def find_user_by_id(id):
    user_list = users_list()
    result_list = []
    for row in user_list:
        if str(row[2]) == id:
            result_list = row
    print(result_list)
    return result_list




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





# cur.execute("""CREATE TABLE IF NOT EXISTS types(
#   type TEXT PRIMARY KEY);
# """)
# conn.commit()

# cur.execute("""INSERT INTO users(name, phone, tgid, role, area)
#   VALUES('Осипов Данил Дмитриевич', '79636871080', '373531147', 'РГ', '4_6');""")
# conn.commit()

# cur.execute("""INSERT OR REPLACE INTO types(type) VALUES('Cable 305m');""")
# conn.commit()
# cur.execute("SELECT * FROM types;")
# one_result = cur.fetchall()
# print(one_result)
