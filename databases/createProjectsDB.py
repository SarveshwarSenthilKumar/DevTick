import sqlite3
import os

database = open('../databases/projects.db', 'w')
database.truncate(0)  
database.close()
connection = sqlite3.connect("../databases/projects.db")
crsr = connection.cursor()

fields = [
    #Basic Information for API Key storage
          "ownedBy", #Store ID of person who made the account
          "additionalFields", #Set up additional fields separated by a comma
          "additionalValues", #Used to store the values for the additional fields
          "title", 
          "description", 
          "category", 
          "status", #Planning, Active, Completed, On Hold, or Archived 
          "techStack",
          "repoLink",
          "contributors",
          "role",
          "startDate",
          "endDate",
          "notes",
          "futurePlans",
          "isActive"
        ]


#Easily convertible to MySQL or other databases due to iterative strategy as opposed to hardcoding the db create string, also improves readability and ease of maintenance and adding new fields

dbCreateString = "CREATE TABLE projects (id INTEGER, "

for field in fields:
    dbCreateString += field+", "

dbCreateString+="PRIMARY KEY(id))"

crsr.execute(dbCreateString)
connection.commit()
crsr.close()
connection.close()
