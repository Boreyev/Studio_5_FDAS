import face_recognition as fr
import cv2
import os
import pickle

def encodings(images):
    encodings = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode_img = fr.face_encodings(img)[0] #ndarray -- N-dimensional array
        encodings.append(encode_img)
        data = {"encodings": encodings, "names": img_names} #save emcodings along with their names in dictionary data
        f = open("encodings/face_enc", "wb") #use pickle to save data into a file for later use
        f.write(pickle.dumps(data))#to open file in write mode
        f.close()#to close file

path = "face_dataset"
images = [] #list of all imgs we are importing
img_names = [] #list of img names
img_list = os.listdir(path) #returns list of img names with .jpg extension
for img in img_list:
    cur_img = cv2.imread(f'{path}/{img}')
    images.append(cur_img)
    img_names.append(os.path.splitext(img)[0]) #removes extension part of file  


known_encodings = encodings(images)

