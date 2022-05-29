import sqlite3

connection = sqlite3.connect('fdas.sqlite')
cursor = connection.cursor()

connection.execute("drop table student")
connection.execute("drop table image")
connection.execute("drop table paper")
connection.execute("drop table class")
connection.execute("drop table attendance")

connection.commit()