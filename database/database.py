import cv2
import sqlite3

#define connection and cursor
connection = sqlite3.connect('fdas.db') #if database does not exist it will be created

#create cursor to interact with sql commands
cursor = connection.cursor()

 #create table
cursor.execute("CREATE TABLE images(id string, image blob)")
connection.commit()

 #load img
cv2.imread('cat.jpg')
cat_img = open( 'cat.jpg', 'rb' ).read()

#insert to db
cursor.execute("insert into images values(?,?)",("pattern",sqlite3.Binary(cat_img)))

connection.commit()


