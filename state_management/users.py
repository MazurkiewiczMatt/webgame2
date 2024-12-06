import json
import os
from flask import jsonify


# Path to the JSON file that stores user data
USER_DATA_FILE = 'users.json'

# Ensure the JSON file exists
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_users():
    """Load user data from the JSON file."""
    with open(USER_DATA_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Save user data to the JSON file."""
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(users, f)

def validate_user(username, session_id, active_sessions):
    if not username or not session_id:
        return jsonify({'status': 'error', 'message': 'Username and session ID are required'}), 400

    if username not in active_sessions or active_sessions[username] != session_id:
        return jsonify({'status': 'error', 'message': 'Invalid session ID'}), 400