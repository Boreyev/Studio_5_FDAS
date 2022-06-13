import sqlite3

def clear_csv():
    filename = "attendance.csv"
# opening the file with w+ mode truncates the file
    f = open(filename, "w")
    f.truncate()
    f.close()

def clear_attendance():
    conn = sqlite3.connect('fdas.sqlite')
    c = conn.cursor()
    c.execute('DELETE FROM attendance')
    #print(c.rowcount, 'records have been deleted from the table.')		
    conn.commit()
    conn.close()

