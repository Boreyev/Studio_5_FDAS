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
    q1 = "select student_id from attendance"
    cur = connection.cursor()
    cur.execute(q1)
    student_id = cur.fetchall()
    for i in range(len(student_id)):
        student_id[i] = str(student_id[i][0])
        cv2.putText(Verti, 'Student ID: ' + student_id[i], (510, y1), font, 0.3, (255, 255, 255), 1)
        y1 += 15
    y2 = 90
    q2 = "select name from attendance"
    cur = connection.cursor()
    cur.execute(q2)
    name = cur.fetchall()
    for i in range(len(name)):
        name[i] = str(name[i][0])
        cv2.putText(Verti, 'Names: ' + name[i], (510, y2), font, 0.3, (255, 255, 255), 1)
        y2 += 15
    y3 = 140
    q3 = "select arrival_time from attendance"
    cur = connection.cursor()
    cur.execute(q3)
    arrival_time = cur.fetchall()
    for i in range(len(arrival_time)):
        arrival_time[i] = str(arrival_time[i][0])
        cv2.putText(Verti, 'arrival time: ' + arrival_time[i], (510, y3), font, 0.3, (255, 255, 255), 1)
        y3 += 15