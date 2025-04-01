
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_session import Session
from datetime import datetime
import pytz
from sql import * #Used for database connection and management
from SarvAuth import * #Used for user authentication functions
from auth import auth_blueprint

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

autoRun = True #Change to True if you want to run the server automatically by running the app.py file
port = 5000 #Change to any port of your choice if you want to run the server automatically
authentication = True #Change to False if you want to disable user authentication

if authentication:
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

#This route is the base route for the website which renders the index.html file
@app.route("/", methods=["GET", "POST"])
def index():
    if not authentication:
        return render_template("index.html")
    else:
        if not session.get("name"):
            return render_template("index.html", authentication=True)
        else:
            return render_template("/auth/loggedin.html")

if autoRun:
    if __name__ == '__main__':
        app.run(debug=True, port=port)
