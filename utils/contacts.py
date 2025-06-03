from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
from flask_session import Session
from datetime import datetime
import pytz
from utils.sql import * #Used for database connection and management
import json
import traceback

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
    
@contacts_blueprint.route("/editcontact/<int:contact_id>", methods=["POST"])
def edit_contact(contact_id):
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/contacts.db")
    
    contact = db.execute("SELECT id FROM contacts WHERE id = :id AND ownedBy = :owner", 
                     id=contact_id, owner=session.get("id"))
    if not contact:
        db = SQL("sqlite:///databases/contacts.db")
        contacts = db.execute("SELECT * FROM contacts WHERE ownedBy = :id", id=session.get("id"))

        for contact in contacts:
            contact["additionalFields"] = json.loads(contact["additionalFields"])
            contact["additionalValues"] = json.loads(contact["additionalValues"])

        return render_template("viewContacts.html", contacts=contacts, error="Task cannot be found!")
    
    additional_fields = request.form.getlist('additionalFields[]')
    additional_values = request.form.getlist('additionalValues[]')
    
    db.execute("UPDATE contacts SET name = :name, nickname = :nickname, company = :company, role = :role, description = :description, emailAddress = :email, address = :address, phoneNumber = :phone, dateOfBirth = :birthDate, gender = :gender, GitHub = :github, LinkedIn = :linkedin, website = :website, additionalFields = :additionalFields, additionalValues = :additionalValues WHERE id = :id AND ownedBy = :owner", name=request.form.get("name"), nickname=request.form.get("nickname"), company=request.form.get("company"), role=request.form.get("role"), description=request.form.get("description"), email=request.form.get("email"), address=request.form.get("address"), phone=request.form.get("phone"), birthDate=request.form.get("birthDate"), gender=request.form.get("gender"), github=request.form.get("github"), linkedin=request.form.get("linkedin"), website=request.form.get("website"), additionalFields=json.dumps(additional_fields), additionalValues=json.dumps(additional_values), id=contact_id, owner=session.get("id"))
    
    db = SQL("sqlite:///databases/contacts.db")
    contacts = db.execute("SELECT * FROM contacts WHERE ownedBy = :id AND status != :status", id=session.get("id"), status="Deleted")

    for contact in contacts:
        contact["additionalFields"] = json.loads(contact["additionalFields"])
        contact["additionalValues"] = json.loads(contact["additionalValues"])

    return render_template("viewContacts.html", contacts=contacts)

@contacts_blueprint.route("/checkdeleted", methods=["GET"])
def viewdeleted():
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/contacts.db")
    contacts = db.execute("SELECT * FROM contacts WHERE ownedBy = :id AND status = :status", id=session.get("id"), status="Deleted")

    for contact in contacts:
        contact["additionalFields"] = json.loads(contact["additionalFields"])
        contact["additionalValues"] = json.loads(contact["additionalValues"])

    return render_template("viewContacts.html", contacts=contacts, deleted=True)

@contacts_blueprint.route("/deletecontact/<int:contact_id>", methods=["POST"])
def delete_contact(contact_id):
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/contacts.db")
    
    contact = db.execute("SELECT id FROM contacts WHERE id = :id AND ownedBy = :owner", 
                     id=contact_id, owner=session.get("id"))
    if not contact:
        db = SQL("sqlite:///databases/contacts.db")
        contacts = db.execute("SELECT * FROM contacts WHERE ownedBy = :id", id=session.get("id"))

        for contact in contacts:
            contact["additionalFields"] = json.loads(contact["additionalFields"])
            contact["additionalValues"] = json.loads(contact["additionalValues"])

        return render_template("viewContacts.html", contacts=contacts, error="Task cannot be found!")
    
    else:
        db.execute("UPDATE contacts SET status = :status WHERE id = :id AND ownedBy = :owner", status="Deleted", id=contact_id, owner=session.get("id"))

    db = SQL("sqlite:///databases/contacts.db")
    contacts = db.execute("SELECT * FROM contacts WHERE ownedBy = :id AND status != :status", id=session.get("id"), status="Deleted")

    for contact in contacts:
        contact["additionalFields"] = json.loads(contact["additionalFields"])
        contact["additionalValues"] = json.loads(contact["additionalValues"])

    return render_template("viewContacts.html", contacts=contacts, error="Contact has been deleted successfully!", success=True)

@contacts_blueprint.route("/recovercontact/<int:contact_id>", methods=["GET", "POST"])
def recover_contact(contact_id):
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/contacts.db")
    
    contact = db.execute("SELECT id FROM contacts WHERE id = :id AND ownedBy = :owner", 
                     id=contact_id, owner=session.get("id"))
    if not contact:
        db = SQL("sqlite:///databases/contacts.db")
        contacts = db.execute("SELECT * FROM contacts WHERE ownedBy = :id", id=session.get("id"))

        for contact in contacts:
            contact["additionalFields"] = json.loads(contact["additionalFields"])
            contact["additionalValues"] = json.loads(contact["additionalValues"])

        return render_template("viewContacts.html", contacts=contacts, error="Contact cannot be found!")
    
    else:
        tz_NY = pytz.timezone('America/New_York') 
        now = datetime.now(tz_NY)
        recoveredOn = now.strftime("%d/%m/%Y %H:%M:%S")

        status = "Recovered on " + recoveredOn

        db.execute("UPDATE contacts SET status = :status WHERE id = :id AND ownedBy = :owner", status=status, id=contact_id, owner=session.get("id"))

    db = SQL("sqlite:///databases/contacts.db")
    tasks = db.execute("SELECT * FROM contacts WHERE ownedBy = :id AND status != :status", id=session.get("id"), status="Deleted")

    for contact in tasks:
        contact["additionalFields"] = json.loads(contact["additionalFields"])
        contact["additionalValues"] = json.loads(contact["additionalValues"])

    return render_template("viewContacts.html", contacts=contacts, error="Contact has been recovered successfully!", success=True)

@contacts_blueprint.route("/search", methods=["POST"])
def search_contacts():
    if not session.get("name"):
        return jsonify({"error": "Not authenticated"}), 401
    
    search_term = request.json.get("search_term", "").strip()
    if not search_term:
        return jsonify({"error": "No search term provided"}), 400
    
    try:
        db = SQL("sqlite:///databases/contacts.db")
        contacts = db.execute("""
            SELECT * FROM contacts 
            WHERE ownedBy = :id 
            AND status != :status
            AND (
                name LIKE :term 
                OR emailAddress LIKE :term 
                OR company LIKE :term
            )
        """, id=session.get("id"), status="Deleted", term=f"%{search_term}%")
        
        for contact in contacts:
            contact["additionalFields"] = json.loads(contact["additionalFields"])
            contact["additionalValues"] = json.loads(contact["additionalValues"])
        
        return jsonify({"contacts": contacts})
    except Exception as e:
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"Error in search_contacts: {error_details}")
        return jsonify({"error": error_details}), 500

@contacts_blueprint.route("/getContactsJson", methods=["GET"])
def getContactsJson():
    if not session.get("name"):
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        db = SQL("sqlite:///databases/contacts.db")
        contacts = db.execute("SELECT * FROM contacts WHERE ownedBy = :id AND status != :status", 
                           id=session.get("id"), status="Deleted")

        for contact in contacts:
            contact["additionalFields"] = json.loads(contact["additionalFields"])
            contact["additionalValues"] = json.loads(contact["additionalValues"])

        return jsonify({"contacts": contacts})
    except Exception as e:
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"Error in getContactsJson: {error_details}")
        return jsonify({"error": error_details}), 500

