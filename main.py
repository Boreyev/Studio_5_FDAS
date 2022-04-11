from cgitb import small
from time import sleep
import time
import face_recognition as fr
import numpy as np
import cv2
import datetime

ptime = 0 #Time = 0
webcam = cv2.VideoCapture(0) #takes video from webcam
font = cv2.FONT_HERSHEY_SIMPLEX #font for all writing

def make_480p():    #Adjusts the camera input to 480p, saves resources. CANNOT BE UPSCALED!
    webcam.set(3, 640)
    webcam.set(4, 480)

belle = fr.load_image_file("dataset/belle_frontal_brow.jpg", mode='RGB') #Load image, convert to RGB on import
#face encoding
belleFaceEncoding = fr.face_encodings(belle)[0]

Ike = fr.load_image_file("dataset/Ike_frontal_brow.jpg", mode='RGB') 
ikeFaceEncoding = fr.face_encodings(Ike,)[0]

known_faces_encodings= [belleFaceEncoding, ikeFaceEncoding]
known_face_names = ["belle", "Ike"]

#detector = fr.get_frontal_face_detector() #detects the coordinate of faces

while True: #Loop to start taking all the frameworks from the camera
    ret, frame = webcam.read()

    frame_resize = cv2.resize(frame, (0, 0), fx=1, fy=1)    #Resizes frame by adjusting frame height and width.
                                                                #Note: Reduced frame scale results in faster frames but lower detection accuracy.  
                                                                #This method is left at the default 1, It can be upscaled but is not recommended. 
    rgb_frame = frame_resize[:, :, ::1]                     #convertframe to rgb

    face_locations = fr.face_locations(rgb_frame, model="hog")                  #check where faces are in the frame, uses hog model (faster but less accurate)
    face_encodings = fr.face_encodings(rgb_frame, face_locations, model=small)  #detects which faces are in the frame
    numFaces = len(face_encodings)                                              #Number of faces in frame = length of face_encodings array
    confidence = str(fr.face_encodings)                                         #Confidence estimate is from euclidean distance from each comparison face 

    ctime = time.time() #Method to get fps by getting passed time since beginning and end of each loop
    fps= int(1/(ctime-ptime))
    ptime = ctime

    cv2.rectangle(frame, (0, 0), (100 + 150, 10 + 10), (19, 155, 35), cv2.FILLED) #Add box behind text for visibility

    cv2.putText(frame,
                f'FPS:{fps}',
                (5, 15), 
                font, 0.5, 
                (255, 255, 255), 
                2, 
                2)

    cv2.putText(frame, 
                f'Number of faces: {numFaces}',
                (70, 15), 
                font, 0.5, 
                (255, 255, 255), 
                2, 
                2)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        nTime = datetime.datetime.now().time()
        matches = fr.compare_faces(known_faces_encodings, face_encoding, tolerance=0.6)

        name = "Unknown"

        face_distances = fr.face_distance(known_faces_encodings, face_encoding) #Compares face encodings and tells you how similar the faces are
        confidence = str(face_distances) #Confidence = face_distance of detected face and face_encoding
        best_match_index = np.argmin(face_distances) #Most similar face_distance = the best match

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        
        #Draw rectangles
        cv2.rectangle(frame, (left, top), (right, bottom), (19, 155, 35), 2)
        cv2.rectangle(frame, (left, bottom -15), (right, bottom), (19, 155, 35), cv2.FILLED)

        #Display Text
        cv2.putText(frame, name, (left +3, bottom -3), font, 0.5, (255, 255, 255), 1)
        cv2.putText(frame,f'{confidence}', (left +3, top -6), font, 0.5, (255, 255, 255), 1) #Put confidence interval above frame, split string to display as percentage. 
        
        lines = [str(nTime), name + ': ' + confidence]
        with open('test_data.txt', 'a') as f:
            for line in lines:
                f.write(line)
                f.write('\n')

        cv2.imwrite("live_dataset/"+name+confidence+'.jpg',frame) #Each time face is detected, save image with name and confidence level
        
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