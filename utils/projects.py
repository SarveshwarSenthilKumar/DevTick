from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
from flask_session import Session
from datetime import datetime
import pytz
from utils.sql import * #Used for database connection and management
import json
import traceback

projects_blueprint = Blueprint('projects', __name__)

@projects_blueprint.route("/createproject", methods=["GET", "POST"])
def create_project():
    if not session.get("name"):
        return redirect("/")
    else:
        if request.method == "GET":
            return render_template("project.html")
        elif request.method == "POST":
            additional_field_titles = request.form.getlist('additional_field_title[]')  
            additional_field_values = request.form.getlist('additional_field_value[]')  

            title = request.form.get("title")
            description = request.form.get("description")
            category = request.form.get("category")
            status = request.form.get("status")
            techStack = request.form.get("techStack")
            repoLink = request.form.get("repoLink")
            contributors = request.form.get("contributors")
            role = request.form.get("role")
            startDate = request.form.get("startDate")
            endDate = request.form.get("endDate")
            notes = request.form.get("notes")
            futurePlans = request.form.get("futurePlans")

            db = SQL("sqlite:///databases/projects.db")
            db.execute("INSERT INTO projects (ownedBy, title, description, category, status, techStack, repoLink, contributors, role, startDate, endDate, notes, futurePlans, isActive, additionalFields, additionalValues) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", session.get("id"), title, description, category, status, techStack, repoLink, contributors, role, startDate, endDate, notes, futurePlans, "Active", json.dumps(additional_field_titles), json.dumps(additional_field_values))

            return render_template("sentence.html", sentences=["You have successfully created an project!"])
        
        