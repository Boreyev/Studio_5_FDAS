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
import pickle
import cvui



#displaying attendance

#     with open('attendance.csv', 'r+') as f: #r+ allows reading and writing
#         attendanceData = f.readlines() #read all lines currently in data to avoid repeats
#         roll = [] #empty list for all names that are found
#         for line in attendanceData: #goes through attendance.csv to check which students are present
#             print(line)
#             entry = line.split(',')
#             print(entry[0])
#             print(entry[1])
#             cv2.putText(Verti, 'Name: ' + entry[0], (510, 45), font, 0.3, (255, 255, 255), 1)
#             cv2.putText(Verti, 'Arrival time: ' + entry[1], (510, 65), font, 0.3, (255, 255, 255), 1)

    # connection = sqlite3.connect('fdas.sqlite')
    # q1 = "select student_id from attendance"
    # cur = connection.cursor()
    # cur.execute(q1)
    # student_id = cur.fetchall()
    # for i in range(len(student_id)):
    #     student_id[i] = str(student_id[i][0])
    #     cv2.putText(Verti, 'Student ID: ' + student_id[i], (510, 45), font, 0.3, (255, 255, 255), 1)

    # q2 = "select name from attendance"
    # cur = connection.cursor()
    # cur.execute(q2)
    # name = cur.fetchall()
    # for i in range(len(name)):
    #     name[i] = str(name[i][0])
    #     cv2.putText(Verti, 'Names: ' + name[i], (510, 65), font, 0.3, (255, 255, 255), 1)

    # q3 = "select arrival_time from attendance"
    # cur = connection.cursor()
    # cur.execute(q3)
    # arrival_time = cur.fetchall()
    # for i in range(len(arrival_time)):
    #     arrival_time[i] = str(arrival_time[i][0])
    #    
def display():
        with open('attendance.csv', 'r+') as f: #r+ allows reading and writing
            attendanceData = f.readlines() #read all lines currently in data to avoid repeats
            roll = [] #empty list for all names that are found
        for line in attendanceData: #goes through attendance.csv to check which students are present
            #print(line)
            entry = line.split(',')
            print(entry[1])

display()