from cgitb import small
import time
from unicodedata import name
import face_recognition as fr
import numpy as np
import cv2
import os
from datetime import datetime, date
import sqlite3
import random 

def backup_live_img():

    connection = sqlite3.connect('fdas.sqlite') #if database does not exist it will be created
    q1 = "select student_id from student"
    cur = connection.cursor()
    cur.execute(q1)
    student_id = cur.fetchall()

    for i in range(len(student_id)):
        student_id[i] = str(student_id[i][0])
        print(student_id[i])

    q2 = "select name from student"
    cur = connection.cursor()
    cur.execute(q2)
    student_name = cur.fetchall()

    for i in range(len(student_name)):
        student_name[i] = str(student_name[i][0])
        print(student_name[i])

    path = "live_dataset"
    img_list = os.listdir(path) #returns list of img names with .jpg extension
    img_id = random.randint(0,10000)
    for name in student_name:
        fullpath = f'{path}/{name}'
        print(fullpath)
        if name == student_name[0]:
            student_id = student_id[0]
        elif name == student_name[1]:
            student_id = 102
        elif name == student_name[2]:
            student_id = 103
        img_list = os.listdir(fullpath)
        for img in img_list:
            cur_img = cv2.imread(f'{fullpath}/{img}')
            img_id += 5
            connection.execute("insert into image values(?,?,?)", (img_id, student_id, cur_img))
            connection.commit()

backup_live_img()