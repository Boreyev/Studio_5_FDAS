import cv2
import os
import random
import sqlite3


def add_student():
    connection.execute('''INSERT INTO student(
   student_id, name) VALUES 
   (101, 'Isobella Johnson')''')
    connection.execute('''INSERT INTO student(
   student_id, name) VALUES 
   (102, 'Ike Callaghan')''')
    connection.execute('''INSERT INTO student(
   student_id, name) VALUES 
   (103, 'John Cena')''')
    connection.execute('''INSERT INTO student(
   student_id, name) VALUES 
   (104, 'John Key')''')
    connection.execute('''INSERT INTO student(
   student_id, name) VALUES 
   (105, 'Queen Elizabeth')''')
    connection.commit()

def add_paper():
    connection.execute('''INSERT INTO paper(
   paper_id, paper_name, tutor) VALUES 
   ('IN510', 'Programming1', 'Krissi')''')
    connection.execute('''INSERT INTO paper(
   paper_id, paper_name, tutor) VALUES 
   ('IN511', 'Programming2', 'Joy')''')
    connection.execute('''INSERT INTO paper(
   paper_id, paper_name, tutor) VALUES 
   ('IN610', 'Programming3', 'Grayson')''')
    connection.execute('''INSERT INTO paper(
   paper_id, paper_name, tutor) VALUES 
   ('IN628', 'Programming4', 'Tom')''')
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
   # connection.execute('''INSERT INTO class(
   #class_id, datetime, paper_id) VALUES 
   #(80, 'Friday 1pm', 'IN628')''')
    connection.commit()


def add_face_dataset():
    path = "face_dataset"
    img_list = os.listdir(path) #returns list of img names with .jpg extension
    #n = random.randint(0,12345)
    student_id = 101
    img_id = 200
    for img in img_list:
        cur_img = cv2.imread(f'{path}/{img}')
        connection.execute("insert into image values(?,?,?)", (img_id, student_id, cur_img))
        student_id += 1
        img_id += 5
        connection.commit()

connection = sqlite3.connect('fdas.sqlite')
add_student()
add_paper()
add_class()
add_face_dataset() #add person id column to image table and assign student id to it