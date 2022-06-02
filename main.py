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

#Window defs
MAIN_WINDOW = 'FDAS'
cvui.init(MAIN_WINDOW)
DATA_WINDOW = 'Data'
cvui.watch(DATA_WINDOW)
mainFrame = np.zeros((240, 200, 3), np.uint8)   #Window dims
mainFrame[:] = (64, 64, 64) #Match mainframe with default CV2 BG
subFrame = np.zeros((240, 200, 3), np.uint8)
subFrame[:] = (64, 64, 64)
#Checkbox states
checked = [False]
checked1 = [False]
checked2 = [False]
checked3 = [False]
checked4 = [False]
checked5 = [False]
#TrackBar Value
trackbarValue = [0.5] 
frameWidth = 0.5
frameHeight = 0.5
#OpenCV variables
webcam = cv2.VideoCapture(0) #takes video from webcam
font = cv2.FONT_HERSHEY_SIMPLEX #font for all writing
ptime = 0 #Time = 0

padding = cv2.imread('GUI_Res/Padding.png')

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
        if student_name == student_name[0]:
            student_id = student_id[0]
        elif student_name == student_name[1]:
            student_id = student_id[1]
        elif student_name == student_name[2]:
            student_id = student_name[2]
        img_list = os.listdir(fullpath)
        print(img_list)
        for img in img_list:
            cur_img = cv2.imread(f'{fullpath}/{img}')
            img_id += 5
            connection.execute("insert into image values(?,?,?)", (img_id, student_id, cur_img))
            connection.commit()

def resize_Face(): #Not in use as of now, work in progress 
    img_Height = 100
    img_Width = 80
    img_Dim = img_Width, img_Height

    
def save_Data():    #Outputs face detection data to text file
    lines = [str(nTime) + '\n' + name + ': ' + str(confidence_out)]
    with open('test_data.txt', 'a') as f:
        for line in lines:
            f.write(line)
            f.write('\n')
            f.write('\n')

def save_distances():    #Outputs face detection data to text file
        lines = [str(name) + ' Detected: ' + str(nTime) + '\n' + 'Names: ' + str(img_names) + '\n' + 'Distances: ' + str(face_distances)]
        with open('test_distances.txt', 'a') as f:
            for line in lines:
                f.write(line)
                f.write('\n')
                f.write('\n')

def insert_attendance(name, curDate, arrival_time, id):
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
    
    if arrival_time > classtime[4]:
        classid = 0
        arrival_status = 'ABSENT'
    print(classid)
    print(name)
    print(curDate)
    print(arrival_time)
    print(arrival_status)
    print(id)
    connection.execute("insert into attendance values(?,?,?,?,?,?)", (classid, name, curDate, arrival_time, arrival_status, id))
    connection.commit()

def late_msg():
    cv2.putText(frame, f'YOU ARE LATE!!', (left +5, bottom +25), font, 0.75, (0, 0, 255), 2)  

def check_attendance(name):
    curDate = date.today()
    curDate = str(curDate)
#select student name and id from student table and then if name = studentname[1], = studentid 1
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

    if name == 'Unknown':
        id = 0

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
            insert_attendance(name, curDate, arrival_time, id)



def face_Frame_Visuals():
        cv2.rectangle(Verti, (left, top), (right, bottom), (55, 158, 58), 2)                 #Displays frame around detected face
        cv2.rectangle(Verti, (left, bottom +17), (right, bottom), (55, 158, 58), cv2.FILLED) #Displays box for name visibility
        cv2.putText(Verti, name, (left +3, bottom +15), font, 0.3, (255, 255, 255), 1)        #Displays name
        cv2.putText(Verti,f'{confidence}', (left +3, bottom +8), font, 0.3, (255, 255, 255), 1) #Put distance above frame, split string to display as percentage. 


def display_attendance_data():
    connection = sqlite3.connect('fdas.sqlite')
    q1 = "select student_id from attendance"
    cur = connection.cursor()
    cur.execute(q1)
    student_id = cur.fetchall()
    for i in range(len(student_id)):
        student_id[i] = str(student_id[i][0])

        i+=1
        
    q2 = "select name from attendance"
    cur = connection.cursor()
    cur.execute(q2)
    name = cur.fetchall()
    # for n in name:
    #     aname = ''.join(map(str,name))
    for i in range(len(name)):
        name[i] = str(name[i][0])

    q3 = "select arrival_time from attendance"
    cur = connection.cursor()
    cur.execute(q3)
    arrival_time = cur.fetchall()
    for i in range(len(arrival_time)):
        arrival_time[i] = str(arrival_time[i][0])

    cv2.putText(subFrame, 'Student ID: ' + student_id[i], (40, 25), font, 0.3, (255, 255, 255), 1)
    cv2.putText(subFrame, 'Names: ' + name[i], (40, 90), font, 0.3, (255, 255, 255), 1)
    cv2.putText(subFrame, 'arrival time: ' + arrival_time[i], (40, 135), font, 0.3, (255, 255, 255), 1)



    #look over different for loops and maybe find one t
    #main  
#backup_live_img()
data = pickle.loads(open('encodings/face_enc', "rb").read())
#names = []

     
def save_encoding_Data(face_encoding):    #Outputs face detection data to text file
     lines = [str(face_encoding)]
     with open('encoding_data.txt', 'a') as f:
         for line in lines:
             f.write(line)
             f.write('\n')

def encodings(images):  #Documenting Required
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
    
known_encodings = encodings(images)

while True: #Loop to start taking all the frameworks from the camera
    ret, frame = webcam.read()

    frame_resize = cv2.resize(frame, (0, 0), fx=frameWidth, fy=frameHeight)    #Resizes frame by adjusting frame height and width.
                                                                           #Note: Reduced frame scale results in faster frames but lower detection accuracy.  
                                                                               #This method is left at the default 1, It can be upscaled but is not recommended.                                             #This method is left at the default 1, It can be upscaled but is not recommended. 
    rgb_frame = frame_resize[:, :, ::-1]                        #convertframe to rgb
    
    Hori = np.concatenate((frame_resize, mainFrame), axis=1)    #Merge settings and webcam frame
    Verti = np.concatenate((Hori, padding), axis=0)             #Add bottom padding
   
    face_locations = fr.face_locations(rgb_frame, model="hog")                  #check where faces are in the frame, uses hog model (faster but less accurate)
    face_encodings = fr.face_encodings(rgb_frame, face_locations, num_jitters=1, model=small)  #detects which faces are in the frame
    numFaces = len(face_encodings)                                              #Number of faces in frame = length of face_encodings array

    ctime = time.time() #Method to get fps by getting passed time since beginning and end of each loop
    fps= int(1/(ctime-ptime))
    ptime = ctime

    #Loop through each encoding in DB
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        
        nTime = datetime.now().time()
        matches = fr.compare_faces(data["encodings"], face_encoding, tolerance=trackbarValue) #fix in test
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
        cvui.context(MAIN_WINDOW)
        #If frame box checked, display face_frame visuals
        if checked1 == [False]:
            face_Frame_Visuals()
        else:
            pass

        #If save data box checked, save data    
        if checked2 == [True]:
            save_encoding_Data(face_encoding)
            save_Face()
            save_Data()
            save_distances()
        else:
            pass

    #If Settiing box checked, resize frame to display settings
    if checked3 == [True]:
        cv2.resizeWindow(MAIN_WINDOW, 540, 210)
    else:
        cv2.resizeWindow(MAIN_WINDOW, 320, 210)

    #If info box checked, display info
    if checked == [False]:
        cvui.text(Verti, 5, 182, f'FPS:{fps}', 0.4, 0xcccccc)
        cvui.text(Verti, 70, 182, f'Number of faces: {numFaces}', 0.4, 0xcccccc)
        cvui.text(Verti, 5, 195, f'Last Detected: {name}. ', 0.4, 0xcccccc)
    else:
        pass

    #If pause box checked, pause system, requires holddown of any key to uncheck box (FIX)
    if checked4 == [True]:
        cv2.waitKey()
    else:
        pass

    #Display Visual Info (Settings)
    cvui.checkbox(Verti, 10, 10, 'Pause', checked4)
    cvui.checkbox(Verti, 210, 181, 'Settings', checked3)
    cvui.text(Verti, 340, 5, 'Settings:', 0.6, 0xcccccc)
    cvui.checkbox(Verti, 335, 30, 'Save Data', checked2)
    cvui.checkbox(Verti, 335, 50, 'Hide Box', checked1)
    cvui.checkbox(Verti, 335, 70, 'Hide Information', checked)
    cvui.text(Verti, 360, 95, 'Tolerance Threshold:', 0.4, 0xcccccc)
    cvui.trackbar(Verti, 325, 110, 200, trackbarValue, 0.0, 1)
    


    cvui.update()   #Cvui needs to be updated before performing any cv2 actions
    cv2.imshow(MAIN_WINDOW, Verti)

    #display data to data window
    cvui.context(DATA_WINDOW)
    cvui.checkbox(subFrame, 10, 15, 'Display Present Students:', checked5)
    curTime = datetime.now()
    currentTime = curTime.strftime('%H:%M:%S')
    cv2.putText(subFrame, 'Current time: ' + currentTime, (20, 155), font, 0.3, (255, 255, 255), 1)

    if checked5 == [True]:
        display_attendance_data()
    else:
        pass
    cvui.update()
    cv2.imshow(DATA_WINDOW, subFrame)
    
    #Destroy window if 'q' pressed. (Change to close on 'X' click)
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
#CVUI: https://github.com/Dovyski/cvui/blob/master/example/src/main-app/main-app.py
#Single Window solution: https://www.geeksforgeeks.org/how-to-display-multiple-images-in-one-window-using-opencv-python/

#Dev Notes:
    #Will be worth refactoring code, file for all defs, file for all visual outputs. Keep def calls and logic in Main.py
    #Pause functionality needs polishing
    #Need to increase efficiency on main for loop
    #Better documentation is required
