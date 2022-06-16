from cgitb import small
from tabnanny import check
import time
from unicodedata import name
import face_recognition as fr
import numpy as np
import cv2
import os
from datetime import datetime, date
import sqlite3
import random 
import pickle
import cvui

def check_attendance(name):
    randid = random.randint(5,15)
    curDate = date.today()
    curDate = str(curDate)

    connection = sqlite3.connect('fdas.sqlite')
    q1 = "select student_id from student"
    cur = connection.cursor()
    cur.execute(q1)
    student_id = cur.fetchall()
    for i in range(len(student_id)):
        student_id[i] = str(student_id[i][0])

    q2 = "select name from student"
    cur = connection.cursor()
    cur.execute(q2)
    student_name = cur.fetchall()
    for i in range(len(student_name)):
        student_name[i] = str(student_name[i][0])

    if name == student_name[0]:
        id = student_id[0]

    if name == student_name[1]:
        id = student_id[1]

    if name == student_name[2]:
        id = randid

    with open('roll.csv', 'r+') as f: #r+ allows reading and writing
        attendanceData = f.readlines() #read all lines currently in data to avoid repeats
        roll = [] #empty list for all names that are found
        for line in attendanceData: #goes through attendance.csv to check which students are present
            entry = line.split(',') 
            roll.append(entry[0]) 
        if name not in roll: #if name is already not present...
            curTime = datetime.now()
            arrival_time = curTime.strftime('%H:%M:%S')

            q1 = "select class_id from class"
            cur.execute(q1)
            class_id = cur.fetchall()
            for i in range(len(class_id)):
                class_id[i] = str(class_id[i][0])

            q2 = "select datetime from class"
            cur.execute(q2)
            classtime = cur.fetchall()
            for i in range(len(classtime)):
                classtime[i] = str(classtime[i][0])

            if classtime[0] < arrival_time < classtime[1]:
                classid = class_id[0]
                arrival_status = 'PRESENT'
            if classtime[0] + '00:10:00' < arrival_time < classtime[1]:
                classid = class_id[0]
                arrival_status = 'LATE'

            if classtime[1] < arrival_time < classtime[2]:
                classid = class_id[1]
                arrival_status = 'PRESENT'
            if classtime[1] + '00:10:00' < arrival_time < classtime[2]:
                classid = class_id[1]
                arrival_status = 'LATE'

            if classtime[2] < arrival_time < classtime[3]:
                classid = class_id[2]
                arrival_status = 'PRESENT'
            if classtime[2] + '00:10:00' < arrival_time < classtime[3]:
                classid = class_id[2]
                arrival_status = 'LATE'

            if classtime[3] < arrival_time < classtime[4]:
                classid = class_id[3]
                arrival_status = 'PRESENT'
            if classtime[3] + '00:10:00' < arrival_time < classtime[4]:
                classid = class_id[3]
                arrival_status = 'LATE'
            else:
                classid = 0
                arrival_status = 'LATE'

            f.writelines(f'\n{name}, {arrival_time}, {arrival_status}') #enters name and time attendance is recorded
            connection.execute("insert into attendance values(?,?,?,?,?,?)", (classid, name, curDate, arrival_time, arrival_status, id))
            connection.commit()
                        
