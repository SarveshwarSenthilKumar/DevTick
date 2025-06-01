from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session
from datetime import datetime
import pytz
from utils.sql import * #Used for database connection and management
from utils.SarvAuth import * #Used for user authentication functions
from utils.auth import auth_blueprint
from utils.tasks import tasks_blueprint
from utils.contacts import contacts_blueprint
from utils.keys import keys_blueprint
from utils.chat import chat_blueprint
from utils.projects import projects_blueprint

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

autoRun = True #Change to True if you want to run the server automatically by running the app.py file
port = 5000 #Change to any port of your choice if you want to run the server automatically
authentication = True #Change to False if you want to disable user authentication

if authentication:
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

app.register_blueprint(tasks_blueprint, url_prefix='/tasks') # Set up tasks functionality
app.register_blueprint(contacts_blueprint, url_prefix='/contacts') # Set up contacts functionality
app.register_blueprint(keys_blueprint, url_prefix='/keys') # Set up keys functionality
app.register_blueprint(projects_blueprint, url_prefix='/projects') # Set up projects functionality
app.register_blueprint(chat_blueprint) # Set up chat functionality

#This route is the base route for the website which renders the landing page, then homepage if logged in
@app.route("/", methods=["GET", "POST"])
def index():
    if not authentication:
        return render_template("index.html")
    else:
        if not session.get("name"):
            return render_template("index.html", authentication=True)
        else:
            return render_template("homepage.html")
        
@app.route("/templates", methods=["GET", "POST"])
def templates():
    return render_template("templates.html")

if autoRun:
    if __name__ == '__main__':
        app.run(debug=True, port=port)
