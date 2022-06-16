from cgitb import small
from unicodedata import name
import face_recognition as fr
import numpy as np
import cv2
from datetime import datetime, date
import time
import csv
from clear_data import clear_csv

#Verti, font
def display(Verti, font, scale):
    y = 225
    x = 325
    # if checkedx == [True]:
    #    clear_csv()
    #    cv2.putText(Verti, f'No students present', (x, y), font, 0.3, (255, 255, 255), 1)
    #else:
    with open('roll.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    cv2.putText(Verti, f' {row[0]}, is{row[2]}.', (x*scale, y), font, 0.3, (255, 255, 255), 1)
                    cv2.putText(Verti, f'Arrival time:{row[1]}', (x*scale, (y+15)), font, 0.3, (255, 255, 255), 1)              
                    line_count += 1
                    y += 30

    
