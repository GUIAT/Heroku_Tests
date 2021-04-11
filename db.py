import sqlite3

connection = sqlite3.connect('students.sqlite3')
cursor = connection.cursor()

cursor.execute("SELECT * FROM receivedData")
connection.commit()

connection.close()
