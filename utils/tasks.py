from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
from flask_session import Session
from datetime import datetime
import pytz
from utils.sql import * #Used for database connection and management
import json

tasks_blueprint = Blueprint('tasks', __name__)

@tasks_blueprint.route("/createtask", methods=["GET", "POST"])
def tasks():
    if not session.get("name"):
        return redirect("/")
    else:
        if request.method == "GET":
            return render_template("task.html")
        elif request.method == "POST":
            additional_field_titles = request.form.getlist('additional_field_title[]')  
            additional_field_values = request.form.getlist('additional_field_value[]')  

            title = request.form.get("title")
            description = request.form.get("description")
            category = request.form.get("category")
            assignedTo = request.form.get("assignedTo")
            contributors = request.form.get("contributors")
            priority = request.form.get("priority")
            additionalNotes = request.form.get("additionalNotes")
            dueDate = request.form.get("dueDate")
            project = request.form.get("project")

            tz_NY = pytz.timezone('America/New_York') 
            now = datetime.now(tz_NY)
            createdAt = now.strftime("%d/%m/%Y %H:%M:%S")

            db = SQL("sqlite:///databases/tasks.db")
            db.execute("INSERT INTO tasks (ownedBy, project, additionalFields, additionalValues, title, description, category, status, createdAt, assignedTo, contributors, priority, notes, dueDate) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)", session.get("id"), project, json.dumps(additional_field_titles), json.dumps(additional_field_values), title, description, category, "Active", createdAt, assignedTo, contributors, priority, additionalNotes, dueDate)

            return render_template("sentence.html", sentences=["You have successfully created a task!"])
        
        return render_template("task.html")
            
@tasks_blueprint.route("/getTasks", methods=["GET"])
def getTasks():
    if not session.get("name"):
        return redirect("/")
    else:
        db = SQL("sqlite:///databases/tasks.db")
        tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id", id=session.get("id"))

        for task in tasks:
            task["additionalFields"] = json.loads(task["additionalFields"])
            task["additionalValues"] = json.loads(task["additionalValues"])

        return render_template("viewTasks.html", tasks=tasks)
