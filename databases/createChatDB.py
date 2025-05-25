import sqlite3
import os

database = open('../databases/chat.db', 'w')
database.truncate(0)  
database.close()
connection = sqlite3.connect("../databases/chat.db")
crsr = connection.cursor()

fields = [
    #Basic Information for message storage
    "user_id",      #ID of the user who sent/received the message
    "message",      #The actual message content
    "timestamp",    #When the message was sent
    "is_ai",        #Whether the message is from AI (True) or user (False)
]

#Easily convertible to MySQL or other databases due to iterative strategy as opposed to hardcoding the db create string, also improves readability and ease of maintenance and adding new fields

dbCreateString = "CREATE TABLE messages (id INTEGER, "

for field in fields:
    dbCreateString += field+", "

dbCreateString+="PRIMARY KEY(id))"

crsr.execute(dbCreateString)
connection.commit()
crsr.close()
connection.close() 