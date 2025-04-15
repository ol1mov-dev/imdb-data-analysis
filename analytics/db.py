import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('../movies.sqlite')
conn.row_factory = sqlite3.Row  # Это позволяет обращаться к полям по имени
cursor = conn.cursor()