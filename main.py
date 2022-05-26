from cgitb import small
import time
import face_recognition as fr
import numpy as np
import cv2
import os
from datetime import datetime
import sqlite3
import random 

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
        if name == known_names[1]:
            student_id = known_student_id[1]
        if name == known_names[2]:
            student_id = known_student_id[2]
        img_list = os.listdir(fullpath)
        print(img_list)
        for img in img_list:
            cur_img = cv2.imread(f'{fullpath}/{img}')
            img_id += 5
            connection.execute("insert into image values(?,?,?)", (img_id, student_id, cur_img))
            connection.commit()



# def resize_Face(): #Not in use as of now, work in progress 
#     img_Height = 100
#     img_Width = 100
#     img_Dim = img_Width, img_Height

#     for i in range(5):
#         if i==5:
#             i = 0
#         elif i == 0 or 1 or 2 or 3 or 4:
#             img_Name = cv2.imread("live_dataset/"+name+"/"+name+str(i)+'.jpg')
#             resize_Img = cv2.resize(img_Name, img_Dim, interpolation = cv2.INTER_AREA)
#             save_Img_Resize = cv2.imwrite("live_dataset/"+name+"/"+name+str(i)+'.jpg', resize_Img)
#     return save_Img_Resize
    
def save_Data():    #Outputs face detection data to text file
    lines = [str(nTime), name + ': ' + str(confidence_out)]
    with open('test_data.txt', 'a') as f:
        for line in lines:
            f.write(line)
            f.write('\n')

def insert_attendance(classid, name, arrival_time, classtimes, arrival_status):
    connection = sqlite3.connect('fdas.sqlite')
    class_id = 0

    if classtimes[0] < arrival_time < classtimes[1]:
        class_id = classid[0]
        arrival_status = 'PRESENT'
    if classtimes[0] + '00:10:00' < arrival_time < classtimes[1]:
        class_id = classid[0]
        arrival_status = 'LATE'
        late_msg()

    if classtimes[1] < arrival_time < classtimes[2]:
        class_id = classid[1]
        arrival_status = 'PRESENT'
    if classtimes[1] + '00:10:00' < arrival_time < classtimes[2]:
        class_id = classid[1]
        arrival_status = 'LATE'
        late_msg()

    if classtimes[2] < arrival_time < classtimes[3]:
        class_id = classid[2]
        arrival_status = 'PRESENT'
    if classtimes[2] + '00:10:00' < arrival_time < classtimes[3]:
        class_id = classid[2]
        arrival_status = 'LATE'
        late_msg()

    if classtimes[3] < arrival_time < classtimes[4]:
        class_id = classid[3]
        arrival_status = 'PRESENT'
    if classtimes[3] + '00:10:00' < arrival_time < classtimes[4]:
        class_id = classid[3]
        arrival_status = 'LATE'
        late_msg()

    if arrival_time > classtimes[4]:
        arrival_status = 'ABSENT'
        
    connection.execute("insert into attendance values(?,?,?,?)", (class_id, name, arrival_time, arrival_status))
    connection.commit()

def late_msg():
    cv2.putText(frame, f'YOU ARE LATE!!', (left +5, bottom +25), font, 0.75, (0, 0, 255), 2)  

def check_attendance(name):
    classtimes = ['8:00:00', '10:00:00', '13:00:00', '15:00:00', '17:00:00']
    classid = [10, 20, 30, 40]
    arrival_status = ''
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
            insert_attendance(classid, name, arrival_time, classtimes, arrival_status)




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
     

def save_encoding_Data(face_encoding):    #Outputs face detection data to text file
     lines = [str(face_encoding)]
     with open('encoding_data.txt', 'a') as f:
         for line in lines:
             f.write(line)
             f.write('\n')

def encodings(images):
    list_of_encodings = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode_img = fr.face_encodings(img)[0] #
        list_of_encodings.append(encode_img) 
    return list_of_encodings 


path = "face_dataset"
images = [] #list of all imgs we are importing
img_names = [] #list of img names
img_list = os.listdir(path) #returns list of img names with .jpg extension
for img in img_list:
    cur_img = cv2.imread(f'{path}/{img}')
    images.append(cur_img)
    img_names.append(os.path.splitext(img)[0]) #removes extension part of file  
known_encodings = encodings(images) # save the encodings and read them from a file ! add ids and date where should be 
# why saving images ? encode them automatically 
backup_live_img()



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
        matches = fr.compare_faces(known_encodings, face_encoding)
        faces_to_compare = [known_encodings, face_encoding]
        name = "Unknown"

        face_distances = fr.face_distance(known_encodings, face_encoding) #Compares face encodings and tells you how similar the faces are
        best_match_index = np.argmin(face_distances)                            #Most similar face_distance = the best match

        confidence = min(face_distances)                                        #Confidence = minimum distance returned by face_distance list
        confidence_out = str(confidence)

        if matches[best_match_index]:
            name = img_names[best_match_index]
            check_attendance(name)
            save_Face()

        face_Frame_Visuals()
        #save_encoding_Data(face_encoding)


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