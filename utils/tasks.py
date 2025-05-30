from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
from flask_session import Session
from datetime import datetime
import pytz
from utils.sql import * #Used for database connection and management
import json
import traceback

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
        tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id AND status != :status AND status != :status2", id=session.get("id"), status="Deleted", status2="Finished")

        for task in tasks:
            task["additionalFields"] = json.loads(task["additionalFields"])
            task["additionalValues"] = json.loads(task["additionalValues"])

        return render_template("viewTasks.html", tasks=tasks)

@tasks_blueprint.route("/finishtask/<int:task_id>", methods=["POST"])
def finish_task(task_id):
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/tasks.db")
    
    task = db.execute("SELECT * FROM tasks WHERE id = :id AND ownedBy = :owner", 
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
        completedAt = now.strftime("%d/%m/%Y %H:%M:%S")

        db.execute("UPDATE tasks SET status = :status, completedAt = :completedAt WHERE id = :id AND ownedBy = :owner", status="Finished", completedAt=completedAt, id=task_id, owner=session.get("id"))

    db = SQL("sqlite:///databases/tasks.db")
    tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id AND status != :status AND status != :status2", id=session.get("id"), status="Deleted", status2="Finished")

    time1 = datetime.strptime(task[0]["createdAt"], "%d/%m/%Y %H:%M:%S")
    time2 = datetime.strptime(completedAt, "%d/%m/%Y %H:%M:%S")

    # Calculate difference
    difference = time2 - time1  # returns a timedelta

    # Break down difference
    days = difference.days
    hours, remainder = divmod(difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    duration = (f"{days} days, {hours} hours, {minutes} minutes, and {seconds} seconds!")

    for task in tasks:
        task["additionalFields"] = json.loads(task["additionalFields"])
        task["additionalValues"] = json.loads(task["additionalValues"])

    return render_template("viewTasks.html", tasks=tasks, error="Congratulations on finishing the task, it took you " + duration, success=True)

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
    tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id AND status != :status AND status != :status2", id=session.get("id"), status="Deleted", status2="Finished")

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

@tasks_blueprint.route("/checkfinished", methods=["GET", "POST"])
def checkfinished():
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/tasks.db")
    tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id AND status = :status", id=session.get("id"), status="Finished")

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
    tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id AND status != :status AND status != :status2", id=session.get("id"), status="Deleted", status2="Finished")

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
    tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id AND status != :status AND status != :status2", id=session.get("id"), status="Deleted", status2="Finished")

    for task in tasks:
        task["additionalFields"] = json.loads(task["additionalFields"])
        task["additionalValues"] = json.loads(task["additionalValues"])

    return render_template("viewTasks.html", tasks=tasks, error="Task has been recovered successfully!", success=True)
@tasks_blueprint.route("/search", methods=["POST"])
def search_tasks():
    if not session.get("name"):
        return jsonify({"error": "Not authenticated"}), 401
    
    search_term = request.json.get("search_term", "").strip()
    if not search_term:
        return jsonify({"error": "No search term provided"}), 400
    
    try:
        db = SQL("sqlite:///databases/tasks.db")
        tasks = db.execute("""
            SELECT * FROM tasks 
            WHERE ownedBy = :id 
            AND status != :status 
            AND status != :status2
            AND (
                title LIKE :term 
                OR description LIKE :term 
                OR category LIKE :term
            )
        """, id=session.get("id"), status="Deleted", status2="Finished", term=f"%{search_term}%")
        
        for task in tasks:
            task["additionalFields"] = json.loads(task["additionalFields"])
            task["additionalValues"] = json.loads(task["additionalValues"])
        
        return jsonify({"tasks": tasks})
    except Exception as e:
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"Error in search_tasks: {error_details}")
        return jsonify({"error": error_details}), 500

@tasks_blueprint.route("/getTasksJson", methods=["GET"])
def getTasksJson():
    if not session.get("name"):
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        db = SQL("sqlite:///databases/tasks.db")
        tasks = db.execute("SELECT * FROM tasks WHERE ownedBy = :id AND status != :status AND status != :status2", 
                         id=session.get("id"), status="Deleted", status2="Finished")

        for task in tasks:
            task["additionalFields"] = json.loads(task["additionalFields"])
            task["additionalValues"] = json.loads(task["additionalValues"])

        return jsonify({"tasks": tasks})
    except Exception as e:
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"Error in getTasksJson: {error_details}")
        return jsonify({"error": error_details}), 500

