import sqlite3


def users_list():
    conn = sqlite3.connect('orders.db')  # Коннектимся к ДБ
    cur = conn.cursor()  # Создаём курсор
    cur.execute("""SELECT * FROM users;""")  # Отправляем SQL заппрос
    utuple = cur.fetchall()  # Получаем ответ
    ulist = []  # Создаём пустой список
    for elem in utuple:  # Перебираем список кортежей
        newelem = list(elem)  # Преобразуем кортеж в список
        ulist.append(newelem)  # Добавляем в новый список
    print(ulist)
    print(ulist[1][1])
    return ulist  # Возвращаем двумерный список



users_list()

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
