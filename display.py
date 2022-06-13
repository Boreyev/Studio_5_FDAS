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

def display(Verti, font):
    y1 = 40
    connection = sqlite3.connect('fdas.sqlite')
    cur = connection.cursor()
    q1 = "select student_id from attendance"
    cur.execute(q1)
    student_id = cur.fetchall()
    for i in range(len(student_id)):
        student_id[i] = str(student_id[i][0])
        cv2.putText(Verti, 'Student ID: ' + student_id[i], (510, y1), font, 0.3, (255, 255, 255), 1)
        y1 += 15
    y2 = 90
    y4 = 90
    q4 = "select arrival_status from attendance"
    cur.execute(q4)
    arrival_status = cur.fetchall()
    for i in range(len(arrival_status)):
        arrival_status[i] = str(arrival_status[i][0])
        if arrival_status[i] == "LATE":
            cv2.putText(Verti, arrival_status[i], (590, y4), font, 0.3, (0,0,255), 1)
            y4 += 15
    q2 = "select name from attendance"
    cur.execute(q2)
    name = cur.fetchall()
    for i in range(len(name)):
        name[i] = str(name[i][0])
        cv2.putText(Verti, 'Name: ' + name[i], (510, y2), font, 0.3, (255, 255, 255), 1)
        y2 += 15
    y3 = 90
    q3 = "select arrival_time from attendance"
    cur.execute(q3)
    arrival_time = cur.fetchall()
    for i in range(len(arrival_time)):
        arrival_time[i] = str(arrival_time[i][0])
        cv2.putText(Verti, ', arrived at: ' + arrival_time[i], (612, y3), font, 0.3, (255, 255, 255), 1)
        y3 += 15   
