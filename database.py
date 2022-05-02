import cv2
import sqlite3

#define connection and cursor
connection = sqlite3.connect('fdas.db') #if database does not exist it will be created

#create cursor to interact with sql commands
cursor = connection.cursor()

 #create table
cursor.execute("CREATE TABLE attendance(name string, datetime string)")
connection.commit()

 #load img
#cv2.imread('cat.jpg')
#cat_img = open( 'cat.jpg', 'rb' ).read()

#insert to db
#create_db and tables
connection = sqlite3.connect('fdas.db') #if database does not exist it will be created
cursor = connection.cursor() #create cursor to interact with sql commands
cursor.execute("CREATE TABLE attendance(name string, datetime string)")
connection.commit()