import cv2
import sqlite3
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


def face_Frame_Visuals(Verti, left, right, top, bottom, confidence, font):
        cv2.rectangle(Verti, (left, top), (right, bottom), (55, 158, 58), 2)                 #Displays frame around detected face
        cv2.rectangle(Verti, (left, bottom +17), (right, bottom), (55, 158, 58), cv2.FILLED) #Displays box for name visibility
        cv2.putText(Verti, name, (left +3, bottom +15), font, 0.3, (255, 255, 255), 1)        #Displays name
        cv2.putText(Verti,f'{confidence}', (left +3, bottom +8), font, 0.3, (255, 255, 255), 1) #Put distance above frame, split string to display as percentage. 

def Display_info(Verti, checked, checked1, checked2, checked3, checked4, checked5, trackbarValue):
    cvui.checkbox(Verti, 10, 10, 'Pause', checked4)
    cvui.checkbox(Verti, 210, 181, 'Settings', checked3)
    cvui.text(Verti, 340, 5, 'Settings:', 0.6, 0xcccccc)
    cvui.checkbox(Verti, 335, 30, 'Save Data', checked2)
    cvui.checkbox(Verti, 335, 50, 'Hide Box', checked1)
    cvui.checkbox(Verti, 335, 70, 'Hide Information', checked)
    cvui.text(Verti, 360, 95, 'Tolerance Threshold:', 0.4, 0xcccccc)
    cvui.trackbar(Verti, 325, 110, 200, trackbarValue, 0.0, 1)