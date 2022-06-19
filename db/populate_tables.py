import cv2
import os
import random
import sqlite3

def create_tables():

    connection = sqlite3.connect('fdas.sqlite') #if database does not exist it will be created
    cursor = connection.cursor() #create cursor to interact with sql commands
    cursor.execute("""CREATE TABLE student
(student_id INTEGER PRIMARY KEY,
name string)""")
    cursor.execute("""CREATE TABLE image
(img_id INTEGER PRIMARY KEY,
student_id int,
image string,
FOREIGN KEY(student_id) REFERENCES student(student_id))""")
    cursor.execute("""CREATE TABLE paper
 (paper_id string NOT NULL, 
 paper_name string,
 tutor string,
 PRIMARY KEY(paper_id))""")
    cursor.execute("""CREATE TABLE class
 (class_id int NOT NULL,
 datetime string,
 paper_id int,
 PRIMARY KEY(class_id),
 FOREIGN KEY(paper_id) REFERENCES paper(paper_id))""")
    cursor.execute("""CREATE TABLE attendance
    (class_id int,
    name string, 
    date string, 
    arrival_time string, 
    arrival_status string, 
    student_id int)""")
#cursor.execute("CREATE TABLE attendance(student_id int, class_id int, datetime string, present bool, FOREIGN KEY(student_id) REFERENCES student(student_id),  FOREIGN KEY(class_id) REFERENCES class(class_id))")
    connection.commit()

def add_student():
    connection.execute('''INSERT INTO student(
   name) VALUES 
   ('Belle')''')
    connection.execute('''INSERT INTO student(
   name) VALUES 
   ('Ike')''')
    connection.execute('''INSERT INTO student(
    name) VALUES 
   ('Unknown')''')
    connection.commit()

def add_paper():
    connection.execute('''INSERT INTO paper(
   paper_id, paper_name, tutor) VALUES 
   ('510', 'Programming1', 'Krissi')''')
    connection.execute('''INSERT INTO paper(
   paper_id, paper_name, tutor) VALUES 
   ('511', 'Programming2', 'Joy')''')
    connection.execute('''INSERT INTO paper(
   paper_id, paper_name, tutor) VALUES 
   ('610', 'Programming3', 'Grayson')''')
    connection.execute('''INSERT INTO paper(
   paper_id, paper_name, tutor) VALUES 
   ('628', 'Programming4', 'Tom')''')
    connection.commit()

def add_class():
    connection.execute('''INSERT INTO class(
   class_id, datetime, paper_id) VALUES 
   (10, '8:00:00', 'IN510')''')
    #connection.execute('''INSERT INTO class(
   #class_id, datetime, paper_id) VALUES 
  # (20, 'Tuesday 1pm', 'IN510')''')
    connection.execute('''INSERT INTO class(
   class_id, datetime, paper_id) VALUES 
   (20, '10:00:00', 'IN511')''')
#    connection.execute('''INSERT INTO class(
 #  class_id, datetime, paper_id) VALUES 
  # (40, 'Tuesday 10am', 'IN511')''')
    connection.execute('''INSERT INTO class(
   class_id, datetime, paper_id) VALUES 
   (30, '13:00:00', 'IN610')''')
   # connection.execute('''INSERT INTO class(
   #class_id, datetime, paper_id) VALUES 
  # (60, 'Thursday 1pm', 'IN610')''')
    connection.execute('''INSERT INTO class(
   class_id, datetime, paper_id) VALUES 
   (40, '15:00:00', 'IN628')''')
    connection.execute('''INSERT INTO class(
   class_id, datetime, paper_id) VALUES 
   (0, '17:00:00', 'NULL')''')

    connection.commit()


def add_face_dataset():
    path = "face_dataset"
    img_list = os.listdir(path) #returns list of img names with .jpg extension
    #n = random.randint(0,12345)
    student_id = 1    
    img_id = random.randint(0,10000)
    for img in img_list:
        cur_img = cv2.imread(f'{path}/{img}')
        connection.execute("insert into image values(?,?,?)", (img_id, student_id, cur_img))
        student_id += 1
        img_id += 5
        connection.commit()




connection = sqlite3.connect('fdas.sqlite')
create_tables()
add_student()
add_paper()
add_class()
add_face_dataset() #add person id column to image table and assign student id to it