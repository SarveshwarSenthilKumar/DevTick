from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
from flask_session import Session
from datetime import datetime
import pytz
from utils.sql import * #Used for database connection and management
from utils.SarvAuth import * #Used for user authentication functions

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
        if session.get("name"):
            return redirect("/")
        if request.method == "GET":
            return render_template("/auth/login.html")
        else:
            username = request.form.get("username").strip().lower()
            password = request.form.get("password").strip()

            password = hash(password)

            db = SQL("sqlite:///databases/users.db")
            users=db.execute("SELECT * FROM users WHERE username = :username", username=username)

            if len(users) == 0:
                return render_template("/auth/login.html", error="No account has been found with this username!")
            user = users[0]
            if user["password"] == password:
                session["name"] = username
                session["id"] = user["id"]
                return redirect("/")

            return render_template("/auth/login.html", error="You have entered an incorrect password! Please try again!")
    
@auth_blueprint.route("/signup", methods=["GET", "POST"])
def signup():
    if session.get("name"):
        return redirect("/")
    if request.method=="GET":
        return render_template("/auth/signup.html")
            
    username = request.form.get("username").strip().lower()
    password = request.form.get("password").strip()

    emailAddress = request.form.get("email").strip().lower()
    phoneNumber = request.form.get("phone").strip().lower()
    fullName = request.form.get("name").strip()
    dateOfBirth = request.form.get("dob").strip().lower()
    gender = request.form.get("gender").strip().lower()

    validName = verifyName(fullName)
    if not validName[0]:
        return render_template("/auth/signUp.html", error=validName[1])
    fullName = validName[1]

    db = SQL("sqlite:///databases/users.db")
    results = db.execute("SELECT * FROM users WHERE username = :username", username=username)

    if len(results) != 0:
        return render_template("/auth/signup.html", error="This username is already taken! Please select a different username!")
    if not checkEmail(emailAddress):
        return render_template("/auth/signup.html", error="You have not entered a valid email address!")
    if len(checkUserPassword(username, password)) > 1:
        return render_template("/auth/signup.html", error=checkUserPassword(username, password)[1])
        
    tz_NY = pytz.timezone('America/New_York') 
    now = datetime.now(tz_NY)
    dateJoined = now.strftime("%d/%m/%Y %H:%M:%S")

    password = hash(password)
        
    db = SQL("sqlite:///databases/users.db")
    db.execute("INSERT INTO users (username, password, dateJoined, accountStatus, emailaddress, phoneNumber, name, dateOfBirth, gender) VALUES (?,?,?,?,?,?,?,?,?)", username, password, dateJoined, "Active", emailAddress, phoneNumber, fullName, dateOfBirth, gender)

    db = SQL("sqlite:///databases/users.db")
    users=db.execute("SELECT * FROM users WHERE username = :username", username=username)

    session["name"] = username
    session["id"] = users[0]["id"]
        
    return redirect("/")
    
@auth_blueprint.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")
