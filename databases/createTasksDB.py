import sqlite3
import os

database = open('../databases/tasks.db', 'w')
database.truncate(0)  
database.close()
connection = sqlite3.connect("../databases/tasks.db")
crsr = connection.cursor()

fields = [
    #Basic Information for task storage
          "ownedBy", #Store ID of person who made the account
          "project", #Optional: project in which the task belongs to (ID of Project)
          "additionalFields", #Set up additional fields separated by a comma
          "additionalValues", #Used to store the values for the additional fields
          "title", 
          "description", 
          "category", 
          "status", #Active, Completed, On Hold, or Archived 
          "createdAt",
          "assignedTo",
          "contributors",
          "priority",
          "notes",
          "dueDate",
          "completedAt",
        ]


#Easily convertible to MySQL or other databases due to iterative strategy as opposed to hardcoding the db create string, also improves readability and ease of maintenance and adding new fields

dbCreateString = "CREATE TABLE tasks (id INTEGER, "

for field in fields:
    dbCreateString += field+", "

dbCreateString+="PRIMARY KEY(id))"

crsr.execute(dbCreateString)
connection.commit()
crsr.close()
connection.close()
