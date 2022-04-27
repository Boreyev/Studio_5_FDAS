from cgitb import small
import time
import face_recognition as fr
import numpy as np
import cv2
from datetime import datetime
from pathlib import Path; 
import sqlite3

webcam = cv2.VideoCapture(0) #takes video from webcam
font = cv2.FONT_HERSHEY_SIMPLEX #font for all writing
ptime = 0 #Time = 0

def make_480p():    #Adjusts the camera input to 480p, saves resources. CANNOT BE UPSCALED!
    webcam.set(3, 640)
    webcam.set(4, 480)

def save_Face():    #Each time face is detected, save image with name and confidence level
    return cv2.imwrite("live_dataset/"+name+"/"+name+str(confidence_out)+'.jpg',frame) 

def save_Data():    #Outputs face detection data to text file
    lines = [str(nTime), name + ': ' + str(confidence_out)]
    with open('test_data.txt', 'a') as f:
        for line in lines:
            f.write(line) 
            f.write('\n')

def attendance(name):
    with open('Attendance.csv', 'r+') as f: #r+ allows reading and writing
        attendanceData = f.readlines() #read all lines currently in data to avoid repeats
        roll = [] #empty list for all names that are found
        for line in attendanceData: #goes through attendance.csv to check which students are present
            entry = line.split(',') 
            roll.append(entry[0]) 
        if name not in roll: #if name is already not present...
            curTime = datetime.now()
            arrival_time = curTime.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {arrival_time}') #enters name and time attendance is recorded
            #attendanceQuery(name, arrival_time)

#def attendanceQuery(name, datetime):
    #connection = sqlite3.connect('fdas.db') #if database does not exist it will be created

#create cursor to interact with sql commands
   # cursor = connection.cursor()

 #create table
   # cursor.execute("CREATE TABLE attendance(name string, datetime string)")
   # connection.commit()

    #sqlite_insert_query = """INSERT INTO attendance
                        #  (name, datetime) 
                         #  VALUES 
                         # ({name}, {datetime})"""

#  #count = cursor.execute(sqlite_insert_query)
 #connection.commit()
  #  print("Record inserted successfully into table")
    #cursor.close()
   # connection.commit()


def frame_Visuals():
    cv2.rectangle(frame, (0, 0), (100 + 150, 10 + 10), (19, 155, 35), cv2.FILLED) #Add box behind text for visibility
    cv2.putText(frame,                                                            #Displays FPS 
                f'FPS:{fps}',
                (5, 15), 
                font, 0.5, 
                (255, 255, 255), 
                2, 
                2)
    cv2.putText(frame,                                                            #Displays number of faces
                f'Number of faces: {numFaces}',
                (70, 15), 
                font, 0.5, 
                (255, 255, 255), 
                2, 
                2)

def face_Frame_Visuals():
        cv2.rectangle(frame, (left, top), (right, bottom), (19, 155, 35), 2)                 #Displays frame around detected face
        cv2.rectangle(frame, (left, bottom -15), (right, bottom), (19, 155, 35), cv2.FILLED) #Displays box for name visibility
        cv2.putText(frame, name, (left +3, bottom -3), font, 0.5, (255, 255, 255), 1)        #Displays name
        cv2.putText(frame,f'{confidence}', (left +3, top -6), font, 0.5, (255, 255, 255), 1) #Put confidence interval above frame, split string to display as percentage. 


belle = fr.load_image_file("face_dataset/Belle.jpg", mode='RGB') #Load image, convert to RGB on import
belleFaceEncoding = fr.face_encodings(belle)[0]
belleName = (Path("face_dataset/Belle.jpg").stem)

Ike = fr.load_image_file("face_dataset/Ike.jpg", mode='RGB') 
ikeFaceEncoding = fr.face_encodings(Ike)[0]
ikeName = (Path("face_dataset/Ike.jpg").stem)

#Test_face = fr.load_image_file("dataset/human.jpg", mode='RGB') 
#testFaceEncoding = fr.face_encodings(Test_face)[0]

known_faces_encodings= [belleFaceEncoding, ikeFaceEncoding] #, testFaceEncoding]
known_face_names = [belleName, ikeName] #, "Test_face"]

while True: #Loop to start taking all the frameworks from the camera
    ret, frame = webcam.read()

    frame_resize = cv2.resize(frame, (0, 0), fx=1, fy=1)    #Resizes frame by adjusting frame height and width.
                                                                #Note: Reduced frame scale results in faster frames but lower detection accuracy.  
                                                                #This method is left at the default 1, It can be upscaled but is not recommended. 
    rgb_frame = frame_resize[:, :, ::1]                     #convertframe to rgb

    face_locations = fr.face_locations(rgb_frame, model="hog")                  #check where faces are in the frame, uses hog model (faster but less accurate)
    face_encodings = fr.face_encodings(rgb_frame, face_locations, model=small)  #detects which faces are in the frame
    numFaces = len(face_encodings)                                              #Number of faces in frame = length of face_encodings array

    ctime = time.time() #Method to get fps by getting passed time since beginning and end of each loop
    fps= int(1/(ctime-ptime))
    ptime = ctime

    frame_Visuals()

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        nTime = datetime.now().time()
        matches = fr.compare_faces(known_faces_encodings, face_encoding, tolerance=0.5)
        name = "Unknown"

        face_distances = fr.face_distance(known_faces_encodings, face_encoding) #Compares face encodings and tells you how similar the faces are
        best_match_index = np.argmin(face_distances)                            #Most similar face_distance = the best match

        confidence = min(face_distances)                                        #Confidence = minimum distance returned by face_distance list
        confidence_out = str(confidence)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        
        attendance(name)
        face_Frame_Visuals()
        save_Face()
        save_Data()

    cv2.imshow('webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()

## SOURCES ## 
#Small parts of the initial functionality of this code is derived from the repository found below:
#base: https://github.com/brunocenteno/face_recognition_video_tutorial
#Frame scaling: https://www.codingforentrepreneurs.com/blog/open-cv-python-change-video-resolution-or-scale/
#FPS display snippet from: https://www.geeksforgeeks.org/yawn-detection-using-opencv-and-dlib/ 
#Append to text file: https://www.pythontutorial.net/python-basics/python-write-text-file/
#face_recognition documentation: https://face-recognition.readthedocs.io/en/latest/face_recognition.html