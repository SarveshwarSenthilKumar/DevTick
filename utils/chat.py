from flask import Flask, render_template, request, redirect, session, jsonify, Blueprint
from flask_session import Session
from datetime import datetime
import pytz
from utils.sql import * #Used for database connection and management
import json
import os
import openai
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential
import traceback

# Load environment variables
load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv('OPENAI_KEY')

chat_blueprint = Blueprint('chat', __name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def get_ai_response(messages):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        return response
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise

@chat_blueprint.route("/send_message", methods=["POST"])
def send_message():
    if not session.get("name"):
        return jsonify({"error": "Not authenticated"}), 401
    
    message = request.json.get("message")
    if not message:
        return jsonify({"error": "No message provided"}), 400
    
    # Get current timestamp in EST
    tz_NY = pytz.timezone('America/New_York') 
    now = datetime.now(tz_NY)
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    
    # Store user message in database
    db = SQL("sqlite:///databases/chat.db")
    db.execute("""
        INSERT INTO messages (user_id, message, timestamp, is_ai)
        VALUES (?, ?, ?, ?)
    """, session.get("id"), message, timestamp, False)
    
    try:
        # Create messages for the AI
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant focused on helping with coding and development tasks. Provide clear, concise, and accurate responses. When sharing code, wrap it in triple backticks with the language specified (e.g., ```python). When sharing a file, indicate it with [FILE] prefix."},
            {"role": "user", "content": message}
        ]
        
        # Get AI response with retry logic
        response = get_ai_response(messages)
        ai_response = response.choices[0].message.content
        
        # Detect if response contains code blocks or files
        contains_code = "```" in ai_response
        contains_file = "[FILE]" in ai_response
        
        # Store AI response in database
        db.execute("""
            INSERT INTO messages (user_id, message, timestamp, is_ai)
            VALUES (?, ?, ?, ?)
        """, session.get("id"), ai_response, timestamp, True)
        
        return jsonify({
            "user_message": {
                "message": message,
                "timestamp": timestamp
            },
            "ai_response": {
                "message": ai_response,
                "timestamp": timestamp,
                "contains_code": contains_code,
                "contains_file": contains_file
            }
        })
        
    except Exception as e:
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"Error in send_message: {error_details}")
        
        # Store error message in database
        error_message = "I apologize, but I encountered an error. Please try again."
        db.execute("""
            INSERT INTO messages (user_id, message, timestamp, is_ai)
            VALUES (?, ?, ?, ?)
        """, session.get("id"), error_message, timestamp, True)
        
        return jsonify({
            "user_message": {
                "message": message,
                "timestamp": timestamp
            },
            "ai_response": {
                "message": error_message,
                "timestamp": timestamp,
                "contains_code": False,
                "contains_file": False
            },
            "error": error_details
        })

@chat_blueprint.route("/get_messages", methods=["GET"])
def get_messages():
    if not session.get("name"):
        return jsonify({"error": "Not authenticated"}), 401
    
    try:
        db = SQL("sqlite:///databases/chat.db")
        messages = db.execute("""
            SELECT message, timestamp, is_ai 
            FROM messages 
            WHERE user_id = ? 
            ORDER BY timestamp ASC
            LIMIT 50
        """, session.get("id"))
        
        return jsonify({"messages": messages})
    except Exception as e:
        error_details = {
            "error": str(e),
            "traceback": traceback.format_exc()
        }
        print(f"Error in get_messages: {error_details}")
        return jsonify({"error": error_details}), 500 
    
    