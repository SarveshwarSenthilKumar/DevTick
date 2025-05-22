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
        keys = db.execute("SELECT * FROM apikeys WHERE ownedBy = :id and isActive != :deleted", id=session.get("id"), deleted="Deleted") 
        
        for key in keys:
            key["additionalFields"] = json.loads(key["additionalFields"])
            key["additionalValues"] = json.loads(key["additionalValues"])

        return render_template("viewKeys.html", keys=keys)

@keys_blueprint.route("/deletekey/<int:key_id>", methods=["POST"])
def delete_key(key_id):
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/apikeys.db")
    
    key = db.execute("SELECT id FROM apikeys WHERE id = :id AND ownedBy = :owner", 
                     id=key_id, owner=session.get("id"))
    if not key:
        db = SQL("sqlite:///databases/apikeys.db")
        keys = db.execute("SELECT * FROM apikeys WHERE ownedBy = :id", id=session.get("id"))

        for key in keys:
            key["additionalFields"] = json.loads(key["additionalFields"])
            key["additionalValues"] = json.loads(key["additionalValues"])

        return render_template("viewKeys.html", keys=keys, error="Task cannot be found!")
    
    else:
        db.execute("UPDATE apikeys SET isActive = :status WHERE id = :id AND ownedBy = :owner", status="Deleted", id=key_id, owner=session.get("id"))

    db = SQL("sqlite:///databases/apikeys.db")
    keys = db.execute("SELECT * FROM apikeys WHERE ownedBy = :id AND isActive != :status", id=session.get("id"), status="Deleted")

    for key in keys:
        key["additionalFields"] = json.loads(key["additionalFields"])
        key["additionalValues"] = json.loads(key["additionalValues"])

    return render_template("viewKeys.html", keys=keys, error="Key has been deleted successfully!", success=True)

@keys_blueprint.route("/editkey/<int:key_id>", methods=["POST"])
def edit_key(key_id):
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/apikeys.db")
    
    key = db.execute("SELECT id FROM apikeys WHERE id = :id AND ownedBy = :owner", 
                     id=key_id, owner=session.get("id"))
    if not key:
        db = SQL("sqlite:///databases/apikeys.db")
        keys = db.execute("SELECT * FROM apikeys WHERE ownedBy = :id", id=session.get("id"))

        for key in keys: 
            key["additionalFields"] = json.loads(key["additionalFields"])
            key["additionalValues"] = json.loads(key["additionalValues"])

        return render_template("viewKeys.html", keys=keys, error="Task cannot be found!")
    
    additional_fields = request.form.getlist('additionalFields[]')
    additional_values = request.form.getlist('additionalValues[]')
    
    db.execute("UPDATE apikeys SET serviceName = :serviceName, apiKey = :apiKey, description = :description, createdAt = :createdAt, expiresAt = :expiresAt, isActive = :isActive, additionalFields = :additionalFields, additionalValues = :additionalValues WHERE id = :id AND ownedBy = :owner", serviceName=request.form.get("serviceName"), apiKey=request.form.get("apiKey"), description=request.form.get("description"), createdAt=request.form.get("createdAt"), expiresAt=request.form.get("expiresAt"), isActive=request.form.get("isActive"), additionalFields=json.dumps(additional_fields), additionalValues=json.dumps(additional_values), id=key_id, owner=session.get("id"))
    
    db = SQL("sqlite:///databases/apikeys.db")
    keys = db.execute("SELECT * FROM apikeys WHERE ownedBy = :id AND isActive != :status", id=session.get("id"), status="Deleted")

    for key in keys:
        key["additionalFields"] = json.loads(key["additionalFields"])
        key["additionalValues"] = json.loads(key["additionalValues"])

    return render_template("viewKeys.html", keys=keys)

@keys_blueprint.route("/checkdeleted", methods=["GET"])
def viewdeleted():
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/apikeys.db")
    keys = db.execute("SELECT * FROM apikeys WHERE ownedBy = :id AND isActive = :isActive", id=session.get("id"), isActive="Deleted")

    for key in keys:
        key["additionalFields"] = json.loads(key["additionalFields"])
        key["additionalValues"] = json.loads(key["additionalValues"])

    return render_template("viewKeys.html", keys=keys, deleted=True)

@keys_blueprint.route("/recoverkey/<int:key_id>", methods=["GET", "POST"])
def recover_key(key_id):
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/apikeys.db")
    
    key = db.execute("SELECT id FROM apikeys WHERE id = :id AND ownedBy = :owner", 
                     id=key_id, owner=session.get("id"))
    if not key:
        db = SQL("sqlite:///databases/apikeys.db")
        keys = db.execute("SELECT * FROM apikeys WHERE ownedBy = :id", id=session.get("id"))

        for key in keys:
            key["additionalFields"] = json.loads(key["additionalFields"])
            key["additionalValues"] = json.loads(key["additionalValues"])

        return render_template("viewKeys.html", keys=keys, error="Key cannot be found!")
    
    else:
        tz_NY = pytz.timezone('America/New_York') 
        now = datetime.now(tz_NY)
        recoveredOn = now.strftime("%d/%m/%Y %H:%M:%S")

        status = "Recovered on " + recoveredOn

        db.execute("UPDATE apikeys SET isActive = :isActive WHERE id = :id AND ownedBy = :owner", isActive=status, id=key_id, owner=session.get("id"))

    db = SQL("sqlite:///databases/apikeys.db")
    keys = db.execute("SELECT * FROM apikeys WHERE ownedBy = :id AND isActive != :isActive", id=session.get("id"), isActive="Deleted")

    for key in keys:
        key["additionalFields"] = json.loads(key["additionalFields"])
        key["additionalValues"] = json.loads(key["additionalValues"])

    return render_template("viewKeys.html", keys=keys, error="Key has been recovered successfully!", success=True)
#restore 