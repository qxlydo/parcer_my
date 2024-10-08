import json
import sqlite3

# Загрузка данных из JSON файла
with open('data.json', 'r') as file:
    data = json.load(file)

# Создание словарей для каждого интервала
legend = {}
super_rary = {}
epic = {}
rary = {}
ordinary = {}

# Обработка данных и заполнение словарей
for vtuber in data['vtuname']:
    name = vtuber['name']
    subs = vtuber['sub']

    if subs >= 865000:
        legend[name] = subs
    elif subs >= 396000:
        super_rary[name] = subs
    elif subs >= 254000:
        epic[name] = subs
    elif subs >= 182000:
        rary[name] = subs
    else:
        ordinary[name] = subs

# Создаем соединение с базой данных
connection = sqlite3.connect('my_database.sqlite3')
cursor = connection.cursor()

# Создаем таблицу Vtubers
cursor.execute('''
CREATE TABLE IF NOT EXISTS Vtubers (
id INTEGER PRIMARY KEY,
vname TEXT NOT NULL,
subs INTEGER NOT NULL,
point INTEGER
)
''')

# Вставка данных из словарей в таблицу
def insert_vtubers(vtuber_dict, point):
    for name, subs in vtuber_dict.items():
        cursor.execute('''INSERT INTO Vtubers (vname, subs, point) VALUES (?, ?, ?)''', (name, subs, subs / 100))

# Вставка данных из каждого словаря
insert_vtubers(legend, 1)       # Присвоим "1" для легенд
insert_vtubers(super_rary, 2)   # Присвоим "2" для супер-редких
insert_vtubers(epic, 3)         # Присвоим "3" для эпических
insert_vtubers(rary, 4)         # Присвоим "4" для редких
insert_vtubers(ordinary, 5)     # Присвоим "5" для обычных

# Сохраняем изменения и закрываем соединение
connection.commit()
connection.close()
