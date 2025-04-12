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
        tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id AND status != :status", id=session.get("id"), status="Deleted")

        for task in tasks:
            task["additionalFields"] = json.loads(task["additionalFields"])
            task["additionalValues"] = json.loads(task["additionalValues"])

        return render_template("viewTasks.html", tasks=tasks)

@tasks_blueprint.route("/edittask/<int:task_id>", methods=["POST"])
def edit_task(task_id):
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/tasks.db")
    
    task = db.execute("SELECT id FROM tasks WHERE id = :id AND ownedBy = :owner", 
                     id=task_id, owner=session.get("id"))
    if not task:
        db = SQL("sqlite:///databases/tasks.db")
        tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id", id=session.get("id"))

        for task in tasks:
            task["additionalFields"] = json.loads(task["additionalFields"])
            task["additionalValues"] = json.loads(task["additionalValues"])

        return render_template("viewTasks.html", tasks=tasks, error="Task cannot be found!")
    
    additional_fields = request.form.getlist('additionalFields[]')
    additional_values = request.form.getlist('additionalValues[]')
    
    db.execute("UPDATE tasks SET title = :title, description = :description, status = :status, priority = :priority, dueDate = :dueDate, assignedTo = :assignedTo,category = :category, notes = :notes, additionalFields = :additionalFields, additionalValues = :additionalValues WHERE id = :id AND ownedBy = :owner", title=request.form.get("title"), description=request.form.get("description"), status=request.form.get("status"), priority=request.form.get("priority"), dueDate=request.form.get("dueDate"), assignedTo=request.form.get("assignedTo"), category=request.form.get("category"), notes=request.form.get("notes"), additionalFields=json.dumps(additional_fields), additionalValues=json.dumps(additional_values), id=task_id, owner=session.get("id"))
    
    db = SQL("sqlite:///databases/tasks.db")
    tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id AND status != :status", id=session.get("id"), status="Deleted")

    for task in tasks:
        task["additionalFields"] = json.loads(task["additionalFields"])
        task["additionalValues"] = json.loads(task["additionalValues"])

    return render_template("viewTasks.html", tasks=tasks, error="Task has been updated successfully!", success=True)

@tasks_blueprint.route("/checkdeleted", methods=["GET"])
def viewdeleted():
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/tasks.db")
    tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id AND status = :status", id=session.get("id"), status="Deleted")

    for task in tasks:
        task["additionalFields"] = json.loads(task["additionalFields"])
        task["additionalValues"] = json.loads(task["additionalValues"])

    return render_template("viewTasks.html", tasks=tasks, deleted=True)

@tasks_blueprint.route("/deletetask/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/tasks.db")
    
    task = db.execute("SELECT id FROM tasks WHERE id = :id AND ownedBy = :owner", 
                     id=task_id, owner=session.get("id"))
    if not task:
        db = SQL("sqlite:///databases/tasks.db")
        tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id", id=session.get("id"))

        for task in tasks:
            task["additionalFields"] = json.loads(task["additionalFields"])
            task["additionalValues"] = json.loads(task["additionalValues"])

        return render_template("viewTasks.html", tasks=tasks, error="Task cannot be found!")
    
    else:
        db.execute("UPDATE tasks SET status = :status WHERE id = :id AND ownedBy = :owner", status="Deleted", id=task_id, owner=session.get("id"))

    db = SQL("sqlite:///databases/tasks.db")
    tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id AND status != :status", id=session.get("id"), status="Deleted")

    for task in tasks:
        task["additionalFields"] = json.loads(task["additionalFields"])
        task["additionalValues"] = json.loads(task["additionalValues"])

    return render_template("viewTasks.html", tasks=tasks, error="Task has been deleted successfully!", success=True)

@tasks_blueprint.route("/recovertask/<int:task_id>", methods=["GET", "POST"])
def recover_task(task_id):
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/tasks.db")
    
    task = db.execute("SELECT id FROM tasks WHERE id = :id AND ownedBy = :owner", 
                     id=task_id, owner=session.get("id"))
    if not task:
        db = SQL("sqlite:///databases/tasks.db")
        tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id", id=session.get("id"))

        for task in tasks:
            task["additionalFields"] = json.loads(task["additionalFields"])
            task["additionalValues"] = json.loads(task["additionalValues"])

        return render_template("viewTasks.html", tasks=tasks, error="Task cannot be found!")
    
    else:
        tz_NY = pytz.timezone('America/New_York') 
        now = datetime.now(tz_NY)
        recoveredOn = now.strftime("%d/%m/%Y %H:%M:%S")

        status = "Recovered on " + recoveredOn

        db.execute("UPDATE tasks SET status = :status WHERE id = :id AND ownedBy = :owner", status=status, id=task_id, owner=session.get("id"))

    db = SQL("sqlite:///databases/tasks.db")
    tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id AND status != :status", id=session.get("id"), status="Deleted")

    for task in tasks:
        task["additionalFields"] = json.loads(task["additionalFields"])
        task["additionalValues"] = json.loads(task["additionalValues"])

    return render_template("viewTasks.html", tasks=tasks, error="Task has been recovered successfully!", success=True)
