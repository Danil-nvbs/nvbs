import sqlite3
conn = sqlite3.connect('orders.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS equip(
   type TEXT,
   sn TEXT PRIMARY KEY,
   storage_date TEXT,
   executor TEXT,
   take_date TEXT,
   cont_moz TEXT,
   cont_moz_date TEXT,
   cont_ex TEXT,
   cont_ex_date TEXT);
""")
conn.commit()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
   name TEXT,
   phone TEXT,
   tgid INT PRIMARY KEY,
   role TEXT,
   area TEXT);
""")
conn.commit()

#cur.execute("""INSERT INTO users(name, phone, tgid, role, area)
#   VALUES('Осипов Данил Дмитриевич', '79636871080', '373531147', 'РГ', '4_6');""")
#conn.commit()

cur.execute("SELECT * FROM equip;")
one_result = cur.fetchone()
print(one_result)