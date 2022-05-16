import sqlite3

connection = sqlite3.connect('fdas.sqlite')
cursor = connection.cursor()
connection.execute("select name from student")

rows = cursor.fetchall()

print(rows)