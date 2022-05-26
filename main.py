from cgitb import small
import time
import face_recognition as fr
import numpy as np
import cv2
import os
from datetime import datetime
import sqlite3
import random 
import pickle


webcam = cv2.VideoCapture(0) #takes video from webcam
font = cv2.FONT_HERSHEY_SIMPLEX #font for all writing
ptime = 0 #Time = 0

def save_Face():    #Each time face is detected, save image with name and confidence level
    for i in range(5):
        if i==5:
            i = 0
        elif i == 0 or 1 or 2 or 3 or 4:
            height = bottom - top + 15   #Define height / width
            width = right - left
            crop_Face = frame_resize[top:top + height, left:left + width]  #Create new frame, use location encodings to crop face.
            save_Image = cv2.imwrite('live_dataset/'+name+'/'+name+str(i)+'.jpg',crop_Face)
    return save_Image

def backup_live_img():
    connection = sqlite3.connect('fdas.sqlite') #if database does not exist it will be created
    known_names = ["Belle", "Ike", "Unknown"]
    known_student_id = [101, 102, 0]
    path = "live_dataset"
    img_list = os.listdir(path) #returns list of img names with .jpg extension
    img_id = random.randint(0,10000)
    for name in known_names:
        fullpath = f'{path}/{name}'
        if name == known_names[0]:
            student_id = known_student_id[0]
        elif name == known_names[1]:
            student_id = known_student_id[1]
        elif name == known_names[2]:
            student_id = known_student_id[2]
        img_list = os.listdir(fullpath)
        print(img_list)
        for img in img_list:
            cur_img = cv2.imread(f'{fullpath}/{img}')
            img_id += 5
            connection.execute("insert into image values(?,?,?)", (img_id, student_id, cur_img))
            connection.commit()

    
def save_Data():    #Outputs face detection data to text file
    lines = [str(nTime), name + ': ' + str(confidence_out)]
    with open('test_data.txt', 'a') as f:
        for line in lines:
            f.write(line)
            f.write('\n')

def insert_attendance(name, arrival_time):
    connection = sqlite3.connect('fdas.sqlite') #if database does not exist it will be created
    cur = connection.cursor() #create cursor to interact with sql commands

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
    connection.execute("insert into attendance values(?,?,?,?)", (classid, name, arrival_time, arrival_status))
    connection.commit()

def late_msg():
    cv2.putText(frame, f'YOU ARE LATE!!', (left +5, bottom +25), font, 0.75, (0, 0, 255), 2)  

def check_attendance(name):
    with open('attendance.csv', 'r+') as f: #r+ allows reading and writing
        attendanceData = f.readlines() #read all lines currently in data to avoid repeats
        roll = [] #empty list for all names that are found
        for line in attendanceData: #goes through attendance.csv to check which students are present
            entry = line.split(',') 
            roll.append(entry[0]) 
        if name not in roll: #if name is already not present...
            curTime = datetime.now()
            arrival_time = curTime.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {arrival_time}') #enters name and time attendance is recorded
            insert_attendance(name, arrival_time)




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



    #main  
backup_live_img()
data = pickle.loads(open('encodings/face_enc', "rb").read())
#names = []

while True: #Loop to start taking all the frameworks from the camera
    ret, frame = webcam.read()

    frame_resize = cv2.resize(frame, (0, 0), fx=1, fy=1)    #Resizes frame by adjusting frame height and width.
                                                                #Note: Reduced frame scale results in faster frames but lower detection accuracy.  
                                                                #This method is left at the default 1, It can be upscaled but is not recommended. 
    rgb_frame = frame_resize[:, :, ::-1]                     #convertframe to rgb

    face_locations = fr.face_locations(rgb_frame, model="hog")                  #check where faces are in the frame, uses hog model (faster but less accurate)
    face_encodings = fr.face_encodings(rgb_frame, face_locations, model=small)  #detects which faces are in the frame
    numFaces = len(face_encodings)                                              #Number of faces in frame = length of face_encodings array

    ctime = time.time() #Method to get fps by getting passed time since beginning and end of each loop
    fps= int(1/(ctime-ptime))
    ptime = ctime

    frame_Visuals()

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        nTime = datetime.now().time()
        matches = fr.compare_faces(data["encodings"], face_encoding)
        faces_to_compare = [data["encodings"], face_encoding]
        name = "Unknown"

        face_distances = fr.face_distance(data["encodings"], face_encoding) #Compares face encodings and tells you how similar the faces are
        best_match_index = np.argmin(face_distances)                            #Most similar face_distance = the best match

        confidence = min(face_distances)                                        #Confidence = minimum distance returned by face_distance list
        confidence_out = str(confidence)

        if True in matches: # check to see if we have found a match
            matchedIndxs = [i for (i, b) in enumerate(matches) if b] #Find positions at which we get True and store them
            count = {}                                              #function gives you back two loop variables: The count of the current iteration, The value of the item at the current iteration
                                                                    #this will extract the matching indices. ?? Enumerate = listing of all of the elements of a set
                                                                    

            for i in matchedIndxs: # loop over the matched indexes and maintain a count for each recognized face face
                name = data["names"][i] #Check the names at respective indexes we stored in matchedIdxs
                count[name] = count.get(name, 0) + 1 #increase count for the name we got
                name = max(count, key=count.get) #set name which has highest count
                #names.append(name) # will update the list of names
                check_attendance(name)

        face_Frame_Visuals()
        #save_encoding_Data(face_encoding)
        save_Face()

        #resize_Face()
        #save_Data()
  

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
#Face cropping logic: https://www.geeksforgeeks.org/cropping-faces-from-images-using-opencv-python/