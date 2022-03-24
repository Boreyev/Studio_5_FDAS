import numpy as np
import face_recognition as fr
import cv2

webcam = cv2.VideoCapture(0) #takes video from webcam

belle = fr.load_image_file("belle_frontal_brow.jpg")
#face encoding
belleFaceEncoding = fr.face_encodings(belle)[0]

Ike = fr.load_image_file("Ike_frontal_brow.jpg")
ikeFaceEncoding = fr.face_encodings(Ike)[0]

known_faces_encodings= [belleFaceEncoding, ikeFaceEncoding]
known_face_names = ["Belle", "Ike"]

#detector = fr.get_frontal_face_detector() #detects the coordinate of faces

while True: #Loop to start taking all the frameworks from the camera
    ret, frame = webcam.read()

    rgb_frame = frame[:, :, ::-1] #convertframe to rgb


    face_locations = fr.face_locations(rgb_frame) #check where faces are in the scree
    face_encodings = fr.face_encodings(rgb_frame, face_locations) #detects which faces are in the screen

    numFaces = len(face_encodings)
    numFacesStr = str(numFaces)
    numFacesTxt = "Number of faces: " + numFacesStr

    font = cv2.FONT_HERSHEY_SIMPLEX #font for all writing

    cv2.putText(frame, 
                numFacesTxt, 
                (50, 50), 
                font, 1, 
                (0, 255, 255), 
                2, 
                2)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

        matches = fr.compare_faces(known_faces_encodings, face_encoding)

        name = "Unknown"

        face_distances = fr.face_distance(known_faces_encodings, face_encoding) #compares face encodings and tells you how similar the faces are

        best_match_index = np.argmin(face_distances) #most similar face_distance = the best match
        if matches[best_match_index]:
            name = known_face_names[best_match_index]
        
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    cv2.imshow('webcam', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

webcam.release()
cv2.destroyAllWindows()

#ref: https://l.facebook.com/l.php?u=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DlC_y8wD7F3Y%26fbclid%3DIwAR1UhwwdchPDUGxUfe_wTlQndCYBos1kkkpHZA1PyJ0Euc8LhIEAcbco0ZM&h=AT1jjLsnPX-m1pz9eusad48aDDudVJckzcaFIFXYMR20IPxYdEeKjYshm0wtD-ter4BHx1ppQ79boSJ_mzBb-z7joT0mqT_rrnfJBHP6sSapfd6og35sHRAabn5ICkHL9LBazrqXuMsQxrI