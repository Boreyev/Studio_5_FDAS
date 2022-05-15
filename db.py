import sqlite3


connection = sqlite3.connect('fdas.sqlite') #if database does not exist it will be created
cursor = connection.cursor() #create cursor to interact with sql commands

cursor.execute("""CREATE TABLE student
(student_id int NOT NULL,
name string,
PRIMARY KEY(student_id))""")
cursor.execute("""CREATE TABLE image
(img_id int NOT NULL,
image blob,
PRIMARY KEY(img_id))""")
cursor.execute("""CREATE TABLE paper
 (paper_id int NOT NULL, 
 name string,
 tutor string,
 PRIMARY KEY(paper_id))""")
cursor.execute("""CREATE TABLE class
 (class_id int NOT NULL,
 datetime string,
 paper_id int,
 PRIMARY KEY(class_id),
 FOREIGN KEY(paper_id) REFERENCES paper(paper_id))""")
cursor.execute("CREATE TABLE attendance(name string, datetime string)")
# cursor.execute("""CREATE TABLE image
# (img_id int NOT NULL,
# image blob,
# student_id int,
# PRIMARY KEY(img_id),
# FOREIGN KEY(student_id) REFERENCES student(student_id))""")



connection.commit()



