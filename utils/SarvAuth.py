import hashlib
import re
import os
from dotenv import load_dotenv

load_dotenv()
# Authentication Encryption Key (Replace with your actual encryption string)
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

allowedChar = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-'!#$%&()*+,./:;<=>?@[\]^_`{|}~ "

def checkEmail(email):
   regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
   if(re.fullmatch(regex, email)):
    return True
   else:
    return False
   
def verifyName(name):
   names=name.split(" ")
   validName=""

   for name in names:
      invalidElement=any(character in name for character in allowedChar[63:])
      if invalidElement:
         return False, "Your name cannot contain any special elements!"
      if "-" in name:
         splitName=name.split("-")
         name=""
         for namePart in splitName:
            name+=namePart[0].upper()+namePart[1:]+"-"
         name=name[:-1]
      else:
         name=name[0].upper()+name[1:]
      validName+=name+" "
   
   return True, validName[:-1]

def checkUserPassword(username, password):

   if username.lower() in password.lower():
      return False, "Your password cannot contain your username!"
   if len(password)<8:
      return False, "Your password needs to be at least 8 characters!"
    
   for letter in username:
      if letter not in allowedChar:
         return False, "Your username may not contain any symbols or special characters!"
   
   if len(username)<8:
      return False, "Your username needs to be at least 8 characters!"
   
   hasUpper=False
   hasLower=False
   hasNumber=False

   for letter in password: 
      indexOfLetter = allowedChar.index(letter)
      if indexOfLetter < 25:   
         hasLower=True
      elif indexOfLetter < 51:
         hasUpper = True
      elif letter in allowedChar:
         hasNumber=True
      else:
         return False, "Your password may not contain any symbols or special characters!"
        
   if not hasUpper:
      return False, "Your password must contain at least one uppercase letter!"
   elif not hasLower:
      return False, "Your password must contain at least one lowercase letter!"
   elif not hasNumber:
      return False, "Your password must contain at least one uppercase letter!"
   else:
      return [True]

def hash(password):
    hashing_object = hashlib.sha256()
    hashing_object.update((password + ENCRYPTION_KEY).encode())  # Combine password and encryption string
    password_hash = hashing_object.hexdigest()
    return password_hash
