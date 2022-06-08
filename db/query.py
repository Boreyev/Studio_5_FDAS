
import sqlite3

from datetime import datetime, date
from unittest import result

connection = sqlite3.connect('fdas.sqlite') #if database does not exist it will be created
curTime = datetime.now() # current date and time
curDate = date.today()
curDate = str(curDate)
classid = 30
name = "Hermione"
id = 107
arrival_status = 'PRESENT'
arrival_time = curTime.strftime("%m/%d/%Y, %H:%M:%S")
print("date and time:",arrival_time)
connection.execute("insert into attendance values(?,?,?,?,?,?)", (classid, name, curDate, arrival_time, arrival_status, id))
connection.commit()

# Python program to get
# current date
  
  




connection = sqlite3.connect('fdas.sqlite') #if database does not exist it will be created
q1 = "select student_id from student"
cur = connection.cursor()
cur.execute(q1)
student_id = cur.fetchall()
# newSid = ''.join(map(str, student_id))
# newnewSid = ''.join(map(str, newSid))
# print(newnewSid)
# for i in range(len(student_id)):
#     newSid = ''.join(map(str,student_id[i]))

for row in student_id:
    newSid = ''.join(map(str,student_id))
    print(newSid)

# q2 = "select name from student"
# cur = connection.cursor()
# cur.execute(q2)
# student_name = cur.fetchall()
# print(student_name)

# q2 = "select name from student"
# cur = connection.cursor()
# cur.execute(q2)
# results = cur.fetchall()
# hi = ','.join(map(str, results))
# print(hi)

# for row in student_name:
#     print(row)

# result_1d = [row[0] for row in results] 
# for i in range(len(student_name)):
#     student_name[i] = str(student_name[i][0])
#     print(student_name[i])

# path = "live_dataset"
# img_list = os.listdir(path) #returns list of img names with .jpg extension
# img_id = random.randint(0,10000)
# for name in student_name:
#     fullpath = f'{path}/{name}'
#     if student_name == student_name[0]:
#         student_id = student_id[0]
#     elif student_name == student_name[1]:
#         student_id = student_id[1]
#     elif student_name == student_name[2]:
#         student_id = student_name[2]
#     img_list = os.listdir(fullpath)
#     print(img_list)


