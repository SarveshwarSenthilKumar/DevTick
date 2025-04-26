from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
from flask_session import Session
from datetime import datetime
import pytz
from utils.sql import * #Used for database connection and management
import json

contacts_blueprint = Blueprint('contacts', __name__)

@contacts_blueprint.route("/createcontact", methods=["GET", "POST"])
def contact():
    if not session.get("name"):
        return redirect("/")
    else:
        if request.method == "GET":
            return render_template("contact.html")
        elif request.method == "POST":
            additional_field_titles = request.form.getlist('additional_field_title[]')  
            additional_field_values = request.form.getlist('additional_field_value[]')  

            fullName = request.form.get("name")
            nickname = request.form.get("nickname")
            company = request.form.get("company")
            role = request.form.get("role")
            description = request.form.get("description")
            email = request.form.get("email")
            address = request.form.get("address")
            phoneNumber = request.form.get("phone")
            birthDate = request.form.get("birthDate")
            gender = request.form.get("gender")
            github = request.form.get("github")
            linkedin = request.form.get("linkedin")
            website = request.form.get("website")

            db = SQL("sqlite:///databases/contacts.db")
            db.execute("INSERT INTO contacts (ownedBy, name, nickname, company, role, description, emailAddress, address, phoneNumber, dateOfBirth, gender, GitHub, LinkedIn, website, status, additionalFields, additionalValues) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", session.get("id"),fullName, nickname, company, role, description, email, address, phoneNumber, birthDate, gender, github, linkedin, website, "Active", json.dumps(additional_field_titles), json.dumps(additional_field_values))

            return render_template("sentence.html", sentences=["You have successfully created a contact!"])

@contacts_blueprint.route("/getContacts", methods=["GET", "POST"])
def getContacts():
    if not session.get("name"):
        return redirect("/")
    else:
        db = SQL("sqlite:///databases/contacts.db")
        contacts = db.execute("SELECT * FROM contacts WHERE ownedBy = :id AND status != :status", id=session.get("id"), status="Deleted")

        for contact in contacts:
            contact["additionalFields"] = json.loads(contact["additionalFields"])
            contact["additionalValues"] = json.loads(contact["additionalValues"])

        return render_template("viewContacts.html", contacts=contacts)
