from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
from flask_session import Session
from datetime import datetime
import pytz
from utils.sql import * #Used for database connection and management
import json

keys_blueprint = Blueprint('keys', __name__)

@keys_blueprint.route("/createkey", methods=["GET", "POST"])
def create_key():
    if not session.get("name"):
        return redirect("/")
    else:
        if request.method == "GET":
            return render_template("key.html")
        elif request.method == "POST":
            additional_field_titles = request.form.getlist('additional_field_title[]')  
            additional_field_values = request.form.getlist('additional_field_value[]')  

            serviceName = request.form.get("serviceName")
            apiKey = request.form.get("apiKey")
            createdAt = request.form.get("createdDate")
            description = request.form.get("description")
            expirationDate = request.form.get("expiryDate")

            db = SQL("sqlite:///databases/apikeys.db")
            db.execute("INSERT INTO apikeys (ownedBy, serviceName, apiKey, description, createdAt, expiresAt, isActive, additionalFields, additionalValues) VALUES (?,?,?,?,?,?,?,?,?)", session.get("id"), serviceName, apiKey, description, createdAt, expirationDate, "Active", json.dumps(additional_field_titles), json.dumps(additional_field_values))

            return render_template("sentence.html", sentences=["You have successfully created an API key!"])
        
@keys_blueprint.route("/getKeys", methods=["GET", "POST"])
def getKeys():
    if not session.get("name"):
        return redirect("/")
    else:
        db = SQL("sqlite:///databases/apikeys.db")
        keys = db.execute("SELECT * FROM apikeys WHERE ownedBy = :id and isActive = :active", id=session.get("id"), active="Active") 

        for key in keys:
            key["additionalFields"] = json.loads(key["additionalFields"])
            key["additionalValues"] = json.loads(key["additionalValues"])

        return render_template("viewKeys.html", keys=keys)
    

#edit, delete, restore, checkdeleted, 