# authentication.py
from flask import request, jsonify
import uuid

from state_management import load_users, save_users, validate_user


def signup(registered_users):
    """Endpoint for user signup."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400

    if username in registered_users:
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 400

    registered_users[username] = password
    save_users(registered_users)

    return jsonify({'status': 'success', 'message': 'User registered successfully'})

def login(registered_users, active_sessions):
    """Endpoint for user login."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400

    if username not in registered_users or registered_users[username] != password:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 400

    # Check if the user is already logged in
    if username in active_sessions:
        session_id = active_sessions[username]
        return jsonify({'status': 'success', 'message': 'User already logged in', 'session_id': session_id})

    # Generate a new session ID
    session_id = str(uuid.uuid4())
    active_sessions[username] = session_id

    return jsonify({'status': 'success', 'message': 'Login successful', 'session_id': session_id})

def logout(active_sessions):
    """Endpoint for user logout."""
    data = request.get_json()
    username = data.get('username')
    session_id = data.get('session_id')

    validate_user(username, session_id, active_sessions)

    # Remove the user from active sessions
    del active_sessions[username]

    return jsonify({'status': 'success', 'message': 'Logout successful'})
