import sqlite3
import os

database = open('../databases/contacts.db', 'w')
database.truncate(0)  
database.close()
connection = sqlite3.connect("../databases/contacts.db")
crsr = connection.cursor()

fields = [
    #Personal Information for Account Setup and Maintenance
          "ownedBy", #Store ID of person who made the account
          "additionalFields", #Set up additional fields separated by a comma
          "additionalValues", #Used to store the values for the additional fields
          "company", #Company/organization of work
          "nickname",
          "description", #Description of relationship
          "GitHub",
          "role", #Job or otherwise
          "website",
          "LinkedIn",
          "emailAddress",
          "phoneNumber",
          "name", #Full Name
          "dateOfBirth",
          "gender", #Prefer Not to Say or Other
        ]


#Easily convertible to MySQL or other databases due to iterative strategy as opposed to hardcoding the db create string, also improves readability and ease of maintenance and adding new fields

dbCreateString = "CREATE TABLE contacts (id INTEGER, "

for field in fields:
    dbCreateString += field+", "

dbCreateString+="PRIMARY KEY(id))"

crsr.execute(dbCreateString)
connection.commit()
crsr.close()
connection.close()
