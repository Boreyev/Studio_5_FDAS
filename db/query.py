import sqlite3
    
connection = sqlite3.connect('fdas.sqlite') #if database does not exist it will be created
cursor = connection.cursor() #create cursor to interact with sql commands


query = "select student_id from student"
cursor.execute(query)
records = cursor.fetchall()

for row in records:
    print(row[0])

