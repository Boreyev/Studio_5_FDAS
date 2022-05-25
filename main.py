from cgitb import small
import time
from unicodedata import name
import face_recognition as fr
import numpy as np
import cv2
import os
from datetime import datetime
import sqlite3
import cvui
import cv2

#Window defs
MAIN_WINDOW = 'FDAS'
cvui.init(MAIN_WINDOW)
mainFrame = np.zeros((180, 200, 3), np.uint8)   #Window dims
mainFrame[:] = (64, 64, 64) #Match mainframe with default CV2 BG
#Checkbox states
checked = [False]
checked1 = [False]
checked2 = [False]
checked3 = [False]
checked4 = [False]
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

def resize_Face(): #Not in use as of now, work in progress 
    img_Height = 100
    img_Width = 80
    img_Dim = img_Width, img_Height

    for i in range(5):
        if i==5:
            i = 0
        elif i == 0 or 1 or 2 or 3 or 4:
            img_Name = cv2.imread("live_dataset/"+name+"/"+name+str(i)+'.jpg')
            resize_Img = cv2.resize(img_Name, img_Dim, interpolation = cv2.INTER_AREA)
            save_Img_Resize = cv2.imwrite("live_dataset/"+name+"/"+name+str(i)+'.jpg', resize_Img)
    return save_Img_Resize
    
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

def create_db():
    connection = sqlite3.connect('fdas.sqlite') #if database does not exist it will be created
    cursor = connection.cursor() #create cursor to interact with sql commands
    cursor.execute("CREATE TABLE attendance(name string, datetime string)")
    connection.commit()

def add_attendance(name, arrival_time):
    connection = sqlite3.connect('fdas.sqlite')
    cursor = connection.cursor()
    cursor.execute("insert into attendance values(?,?)", (name, arrival_time))

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
            add_attendance(name, arrival_time)

def face_Frame_Visuals():
        cv2.rectangle(Verti, (left, top), (right, bottom), (55, 158, 58), 2)                 #Displays frame around detected face
        cv2.rectangle(Verti, (left, bottom +17), (right, bottom), (55, 158, 58), cv2.FILLED) #Displays box for name visibility
        cv2.putText(Verti, name, (left +3, bottom +15), font, 0.3, (255, 255, 255), 1)        #Displays name
        cv2.putText(Verti,f'{confidence}', (left +3, bottom +8), font, 0.3, (255, 255, 255), 1) #Put distance above frame, split string to display as percentage. 
     
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

        matches = fr.compare_faces(known_encodings, face_encoding, tolerance=trackbarValue)
        name = "Unknown"

        face_distances = fr.face_distance(known_encodings, face_encoding) #Compares face encodings and tells you how similar the faces are
        best_match_index = np.argmin(face_distances)                            #Most similar face_distance = the best match

        confidence = min(face_distances)                                        #Confidence = minimum distance returned by face_distance list
        confidence_out = str(confidence)

        if matches[best_match_index]:
            name = img_names[best_match_index]
    
        attendance(name)

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
    #Will be worth refractoring code, file for all defs, file for all visual outputs. Keep def calls and logic in Main.py
    #Pause functionality needs polishing
    #Need to increase efficiency on main for loop
    #Better documentation is required
