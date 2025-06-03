from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
from flask_session import Session
from datetime import datetime
import pytz
from utils.sql import * #Used for database connection and management
import json
import traceback
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_KEY')

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
        
@projects_blueprint.route("/getProjects", methods=["GET", "POST"])
def getProjects():
    if not session.get("name"):
        return redirect("/")
    else:
        db = SQL("sqlite:///databases/projects.db")
        projects = db.execute("SELECT * FROM projects WHERE ownedBy = :id and isActive != :deleted", id=session.get("id"), deleted="Deleted") 

        for project in projects:
            project["additionalFields"] = json.loads(project["additionalFields"])
            project["additionalValues"] = json.loads(project["additionalValues"])

        return render_template("viewProjects.html", projects=projects)

@projects_blueprint.route("/enhance_project/<int:project_id>", methods=["POST"])
def enhance_project(project_id):
    if not session.get("name"):
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        # Get project details from database
        db = SQL("sqlite:///databases/projects.db")
        project = db.execute("SELECT * FROM projects WHERE id = :id AND ownedBy = :owner", 
                           id=project_id, owner=session.get("id"))
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        project = project[0]  # Get first result
        
        # Create prompt for AI
        prompt = f"""Analyze this project and suggest improvements:
Title: {project['title']}
Description: {project['description']}
Category: {project['category']}
Status: {project['status']}
Tech Stack: {project['techStack']}
Contributors: {project['contributors']}
Role: {project['role']}
Notes: {project['notes']}
Future Plans: {project['futurePlans']}

Please provide specific, actionable suggestions for:
1. Technical improvements
2. Best practices to implement
3. Potential features to add
4. Documentation recommendations
5. Testing strategies

Format the response as a JSON object with these keys:
- technical_improvements: array of strings
- best_practices: array of strings
- new_features: array of strings
- documentation: array of strings
- testing: array of strings"""

        # Get AI response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant focused on software development best practices and project improvement."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        # Parse AI response
        suggestions = json.loads(response.choices[0].message.content)
        
        return jsonify({
            "success": True,
            "suggestions": suggestions
        })
        
    except Exception as e:
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"Error in enhance_project: {error_details}")
        return jsonify({"error": error_details}), 500

@projects_blueprint.route("/apply_suggestion/<int:project_id>", methods=["POST"])
def apply_suggestion(project_id):
    if not session.get("name"):
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        data = request.get_json()
        if not data or 'suggestion' not in data or 'category' not in data:
            return jsonify({"error": "Missing suggestion or category"}), 400
            
        suggestion = data['suggestion']
        category = data['category']
        
        # Get project details
        db = SQL("sqlite:///databases/projects.db")
        project = db.execute("SELECT * FROM projects WHERE id = :id AND ownedBy = :owner", 
                           id=project_id, owner=session.get("id"))
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
            
        project = project[0]
        
        # Apply suggestion based on category
        if category == 'technical_improvements':
            # Add to notes with a technical improvements section
            current_notes = project['notes'] or ""
            new_notes = f"{current_notes}\n\nTechnical Improvements:\n- {suggestion}"
            db.execute("UPDATE projects SET notes = :notes WHERE id = :id", 
                      notes=new_notes, id=project_id)
                      
        elif category == 'best_practices':
            # Add to notes with a best practices section
            current_notes = project['notes'] or ""
            new_notes = f"{current_notes}\n\nBest Practices:\n- {suggestion}"
            db.execute("UPDATE projects SET notes = :notes WHERE id = :id", 
                      notes=new_notes, id=project_id)
                      
        elif category == 'new_features':
            # Add to future plans
            current_plans = project['futurePlans'] or ""
            new_plans = f"{current_plans}\n\nNew Features:\n- {suggestion}"
            db.execute("UPDATE projects SET futurePlans = :plans WHERE id = :id", 
                      plans=new_plans, id=project_id)
                      
        elif category == 'documentation':
            # Add to notes with a documentation section
            current_notes = project['notes'] or ""
            new_notes = f"{current_notes}\n\nDocumentation:\n- {suggestion}"
            db.execute("UPDATE projects SET notes = :notes WHERE id = :id", 
                      notes=new_notes, id=project_id)
                      
        elif category == 'testing':
            # Add to notes with a testing section
            current_notes = project['notes'] or ""
            new_notes = f"{current_notes}\n\nTesting:\n- {suggestion}"
            db.execute("UPDATE projects SET notes = :notes WHERE id = :id", 
                      notes=new_notes, id=project_id)
        
        return jsonify({
            "success": True,
            "message": "Suggestion applied successfully"
        })
        
    except Exception as e:
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"Error in apply_suggestion: {error_details}")
        return jsonify({"error": error_details}), 500

@projects_blueprint.route("/apply_all_suggestions/<int:project_id>", methods=["POST"])
def apply_all_suggestions(project_id):
    if not session.get("name"):
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        data = request.get_json()
        if not data or 'suggestions' not in data:
            return jsonify({"error": "Missing suggestions"}), 400
            
        suggestions = data['suggestions']
        
        # Get project details
        db = SQL("sqlite:///databases/projects.db")
        project = db.execute("SELECT * FROM projects WHERE id = :id AND ownedBy = :owner", 
                           id=project_id, owner=session.get("id"))
        
        if not project:
            return jsonify({"error": "Project not found"}), 404
            
        project = project[0]
        
        # Apply all suggestions
        current_notes = project['notes'] or ""
        current_plans = project['futurePlans'] or ""
        
        # Process each category
        for category, items in suggestions.items():
            if category == 'new_features':
                # Add to future plans
                new_plans = f"{current_plans}\n\nNew Features:"
                for item in items:
                    new_plans += f"\n- {item}"
                db.execute("UPDATE projects SET futurePlans = :plans WHERE id = :id", 
                          plans=new_plans, id=project_id)
            else:
                # Add to notes
                section_name = category.replace('_', ' ').title()
                new_notes = f"{current_notes}\n\n{section_name}:"
                for item in items:
                    new_notes += f"\n- {item}"
                db.execute("UPDATE projects SET notes = :notes WHERE id = :id", 
                          notes=new_notes, id=project_id)
        
        return jsonify({
            "success": True,
            "message": "All suggestions applied successfully"
        })
        
    except Exception as e:
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"Error in apply_all_suggestions: {error_details}")
        return jsonify({"error": error_details}), 500


@projects_blueprint.route("/deleteproject/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/projects.db")
    
    project = db.execute("SELECT id FROM projects WHERE id = :id AND ownedBy = :owner", 
                     id=project_id, owner=session.get("id"))
    if not project:
        db = SQL("sqlite:///databases/projects.db")
        projects = db.execute("SELECT * FROM projects WHERE ownedBy = :id", id=session.get("id"))

        for project in projects:
            project["additionalFields"] = json.loads(project["additionalFields"])
            project["additionalValues"] = json.loads(project["additionalValues"])

        return render_template("viewProjects.html", projects=projects, error="Project cannot be found!")
    
    else:
        db.execute("UPDATE projects SET isActive = :status WHERE id = :id AND ownedBy = :owner", status="Deleted", id=project_id, owner=session.get("id"))

    db = SQL("sqlite:///databases/projects.db")
    projects = db.execute("SELECT * FROM projects WHERE ownedBy = :id AND isActive != :status", id=session.get("id"), status="Deleted")

    for project in projects:
        project["additionalFields"] = json.loads(project["additionalFields"])
        project["additionalValues"] = json.loads(project["additionalValues"])

    return render_template("viewProjects.html", projects=projects, error="Project has been deleted successfully!", success=True)


@projects_blueprint.route("/checkdeleted", methods=["GET"])
def viewdeleted():
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/projects.db")
    projects = db.execute("SELECT * FROM projects WHERE ownedBy = :id AND isActive = :isActive", id=session.get("id"), isActive="Deleted")

    for project in projects:
        project["additionalFields"] = json.loads(project["additionalFields"])
        project["additionalValues"] = json.loads(project["additionalValues"])

    return render_template("viewProjects.html", projects=projects, deleted=True)

@projects_blueprint.route("/recoverproject/<int:project_id>", methods=["GET", "POST"])
def recover_project(project_id):
    if not session.get("name"):
        return redirect("/")
    
    db = SQL("sqlite:///databases/projects.db")
    
    project = db.execute("SELECT id FROM projects WHERE id = :id AND ownedBy = :owner", 
                     id=project_id, owner=session.get("id"))
    if not project:
        db = SQL("sqlite:///databases/projects.db")
        keys = db.execute("SELECT * FROM projects WHERE ownedBy = :id", id=session.get("id"))

        for project in projects:
            project["additionalFields"] = json.loads(project["additionalFields"])
            project["additionalValues"] = json.loads(project["additionalValues"])

        return render_template("viewKeys.html", keys=projects, error="Key cannot be found!")
    
    else:
        tz_NY = pytz.timezone('America/New_York') 
        now = datetime.now(tz_NY)
        recoveredOn = now.strftime("%d/%m/%Y %H:%M:%S")

        status = "Recovered on " + recoveredOn

        db.execute("UPDATE projects SET isActive = :isActive WHERE id = :id AND ownedBy = :owner", isActive=status, id=project_id, owner=session.get("id"))

    db = SQL("sqlite:///databases/projects.db")
    projects = db.execute("SELECT * FROM projects WHERE ownedBy = :id AND isActive != :isActive", id=session.get("id"), isActive="Deleted")

    for project in projects:
        project["additionalFields"] = json.loads(project["additionalFields"])
        project["additionalValues"] = json.loads(project["additionalValues"])

    return render_template("viewProjects.html", projects=projects, error="Project has been recovered successfully!", success=True)


@projects_blueprint.route("/search", methods=["POST"])
def search_projects():
    if not session.get("name"):
        return jsonify({"error": "Not authenticated"}), 401
    
    search_term = request.json.get("search_term", "").strip()
    if not search_term:
        return jsonify({"error": "No search term provided"}), 400
    
    try:
        db = SQL("sqlite:///databases/projects.db")
        projects = db.execute("""
            SELECT * FROM projects 
            WHERE ownedBy = :id 
            AND isActive != :status
            AND (
                title LIKE :term 
                OR description LIKE :term
            )
        """, id=session.get("id"), status="Deleted", term=f"%{search_term}%")
        
        for project in projects:
            project["additionalFields"] = json.loads(project["additionalFields"])
            project["additionalValues"] = json.loads(project["additionalValues"])
        
        return jsonify({"projects": projects})
    except Exception as e:
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"Error in search_keys: {error_details}")
        return jsonify({"error": error_details}), 500
    
#Create Edit Key
