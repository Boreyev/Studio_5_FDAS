import sqlite3
    
connection = sqlite3.connect('fdas.sqlite') #if database does not exist it will be created
cursor = connection.cursor() #create cursor to interact with sql commands

w = "select class_id from class"
cursor.execute(w)
cid_records = cursor.fetchall()

for s in cid_records:
    print(s)

query = "select datetime from class"
cursor.execute(query)
records = cursor.fetchall()
for row in records:
    print(row[0])

