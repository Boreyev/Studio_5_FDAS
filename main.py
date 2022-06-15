from cgitb import small
import time
from unicodedata import name
import face_recognition as fr
import numpy as np
import cv2
from datetime import datetime, date
import pickle
import cvui
from save_data import save_encoding_Data, save_distances, save_Data
from img_backup import backup_live_img
from insert_attendance import check_attendance
from display import display
from clear_data import clear_csv
from screeninfo import get_monitors

#Get monitor dims
for monitor in get_monitors():
    mWidth = monitor.width
    mHeight = monitor.height
    print(str(mWidth) + 'x' + str(mHeight))

#Window defs
MAIN_WINDOW = 'FDAS'
cvui.init(MAIN_WINDOW)
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
checked6 = [False]
checked7 = [False]
checked8 = [False]
checkedx = [False]
checkedy = [False]

#TrackBar Value
trackbarValue = [0.5] 
frameWidth = 0.5
frameHeight = 0.5
#OpenCV variables
webcam = cv2.VideoCapture(0) #takes video from webcam
font = cv2.FONT_HERSHEY_SIMPLEX #font for all writing
ptime = 0 #Time = 0

padding = cv2.imread('GUI_Res/Padding.png')
splash = cv2.imread("GUI_Res/FDAS-logos.jpeg")
colour = 0xcccccc

def save_Face():    #Each time face is detected, save image with name and confidence level
    for i in range(2):
        if i==2:
            i = 0
        elif i == 0 or 1 or 2:
            height = bottom - top + 15   #Define height / width
            width = right - left
            crop_Face = frame_resize[top:top + height, left:left + width]  #Create new frame, use location encodings to crop face.
            save_Image = cv2.imwrite('live_dataset/'+name+'/'+name+str(i)+'.jpg',crop_Face)
    return save_Image
   

def face_Frame_Visuals():
        cv2.rectangle(Verti, (left, top), (right, bottom), (55, 158, 58), 2)                    #Displays frame around detected face
        cv2.rectangle(Verti, (left, bottom +17), (right, bottom), (55, 158, 58), cv2.FILLED)    #Displays box for name visibility
        cv2.putText(Verti, name, (left +3, bottom +15), font, 0.3, (255, 255, 255), 1)          #Displays name
        cv2.putText(Verti,f'{confidence}', (left +3, bottom +8), font, 0.3, (255, 255, 255), 1) #Put distance above frame, split string to display as percentage. 

clear_csv()
backup_live_img()         
data = pickle.loads(open('encodings/face_enc', "rb").read())

while True: #Loop to start taking all the frameworks from the camera
    ret, frame = webcam.read()

    frame_resize = cv2.resize(frame, (0, 0), fx=frameWidth, fy=frameHeight)    #Resizes frame by adjusting frame height and width.
                                                                           #Note: Reduced frame scale results in faster frames but lower detection accuracy.  
                                                                               #This method is left at the default 1, It can be upscaled but is not recommended.                                             #This method is left at the default 1, It can be upscaled but is not recommended. 
    rgb_frame = frame_resize[:, :, ::-1]                        #convertframe to rgb
    
    Hori = np.concatenate((frame_resize, mainFrame), axis=1) 
    Bind = np.concatenate((Hori, subFrame), axis=1)   #Merge settings and webcam frame
    Verti = np.concatenate((Bind, padding), axis=0)             #Add bottom padding
   
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


        face_Frame_Visuals()

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
            save_Data(nTime, name, confidence_out)
            save_distances(name, nTime, face_distances)
        else:
            pass

    if checked5 == [False]:
        cvui.image(Verti, 0, 0, splash)
        cvui.checkbox(Verti, 240, 185, 'Start', checked5)
    elif checked5 == [True]:
        
        #If Settiing box checked, resize frame to display settings
        if (cvui.button(Verti, 275, 181, ">")):
            cv2.resizeWindow(MAIN_WINDOW, 520, 210)
        elif (cvui.button(Verti, 235, 181, "<")):
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

        #Checkbox to change to alt theme 
        if checked7==[True]:
            mainFrame[:] = (133,138,126) #Alt / Green theme
            padding = cv2.imread('GUI_Res/PaddingWhite.png')
            colour = 0xF5E9EC
        elif checked7==[False]:
            mainFrame[:] = (64,64,64) #Standard theme
            padding = cv2.imread('GUI_Res/Padding.png')
            colour = 0xcccccc

        if checked6==[True]:
            cv2.rectangle(Verti,(130,45),(260,110),(64,64,64),-1)
            cvui.text(Verti, 140, 60, 'Exit Application?', 0.3, colour)
            if cvui.button(Verti, 135, 75, "Yes"):
                break
            elif cvui.button(Verti, 200, 75, "No"):
                checked6==[False]

        #display data to data window
    cvui.checkbox(Verti, 510, 15, 'Display Present Students:', checkedy)
    cvui.checkbox(Verti, 615, 180, 'Clear roll', checkedx)
    curTime = datetime.now()
    currentTime = curTime.strftime('%H:%M:%S')
    curDate = date.today()
    curDate = str(curDate)
    cvui.text(Verti, 100, 10, 'Date: ' + curDate, 0.4, 0xcccccc)
    cvui.text(Verti, 100, 23, 'Current Time: ' + currentTime, 0.4, 0xcccccc)

    if checkedx == [True]:
        checkedy = [False]
        clear_csv()
        cv2.putText(Verti, f'Roll cleared.', (510, 40), font, 0.3, (255, 255, 255), 1)
    else:
        pass

    if checkedy == [True]:
        check_attendance(name)
        display(Verti, font)
    else:
        pass


    
    #Display Visual Info (Settings)
    cvui.checkbox(Verti, 10, 10, 'Pause', checked4)
    #cvui.checkbox(Verti, 210, 181, 'Settings', checked3)
    cvui.text(Verti, 340, 5, 'Settings:', 0.6, 0xcccccc)
    cvui.checkbox(Verti, 335, 30, 'Save Data', checked2)
    cvui.checkbox(Verti, 335, 50, 'Hide Box', checked1)
    cvui.checkbox(Verti, 335, 70, 'Hide Information', checked)
    cvui.text(Verti, 360, 95, 'Tolerance Threshold:', 0.4, 0xcccccc)
    cvui.trackbar(Verti, 325, 110, 200, trackbarValue, 0.0, 1)


    #Fullscreen functionality
    if checked8==[True]:
        cv2.resizeWindow(MAIN_WINDOW, mWidth, mHeight)
        Verti = cv2.resize(Verti, dsize=(mWidth, mHeight), interpolation=cv2.INTER_CUBIC)

    elif checked8==[False]:
        pass
    
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
    #Will be worth refactoring code, file for all defs, file for all visual outputs. Keep def calls and logic in Main.py
    #Pause functionality needs polishing
    #Need to increase efficiency on main for loop
    #Better documentation is required