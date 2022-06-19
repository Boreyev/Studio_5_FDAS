import sqlite3

def clear_csv():
    filename = "roll.csv"
# opening the file with w+ mode truncates the file
    f = open(filename, "w")
    f.truncate()
    f.close()

