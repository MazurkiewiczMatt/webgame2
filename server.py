from flask import Flask, request, jsonify
import json
import os, sys
import uuid

app = Flask(__name__)

# Add your specific path if needed for importing
path = '/home/Mazurkiewicz/webgame/webgame2'
if path not in sys.path:
    sys.path.append(path)

# Path to the JSON file that stores user data
USER_DATA_FILE = 'users.json'

# Dictionary to hold active users with session IDs
active_sessions = {}

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

@app.route('/')
def status():
    """Display the names of active players."""
    template = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Server Status</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                color: #333;
                margin: 0;
                padding: 20px;
            }
            .container {
                max-width: 600px;
                margin: 0 auto;
                background: #fff;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }
            h1 {
                color: #007BFF;
            }
            ul {
                list-style-type: none;
                padding: 0;
            }
            li {
                background: #e9e9e9;
                margin: 5px 0;
                padding: 10px;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Server Status</h1>
            <p>Server is running!</p>
            <h2>Active Players:</h2>
            {% if active_players %}
                <ul>
                {% for player in active_players %}
                    <li>{{ player }}</li>
                {% endfor %}
                </ul>
            {% else %}
                <p>No active players.</p>
            {% endif %}
        </div>
    </body>
    </html>
    """
    active_players = list(active_sessions.keys())
    return render_template_string(template, active_players=active_players)

@app.route('/signup', methods=['POST'])
def signup():
    """Endpoint for user signup."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400

    users = load_users()

    if username in users:
        return jsonify({'status': 'error', 'message': 'Username already exists'}), 400

    users[username] = password
    save_users(users)

    return jsonify({'status': 'success', 'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    """Endpoint for user login."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400

    users = load_users()

    if username not in users or users[username] != password:
        return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 400

    # Check if the user is already logged in
    if username in active_sessions:
        session_id = active_sessions[username]
        return jsonify({'status': 'success', 'message': 'User already logged in', 'session_id': session_id})

    # Generate a new session ID
    session_id = str(uuid.uuid4())
    active_sessions[username] = session_id

    return jsonify({'status': 'success', 'message': 'Login successful', 'session_id': session_id})

@app.route('/logout', methods=['POST'])
def logout():
    """Endpoint for user logout."""
    data = request.get_json()
    username = data.get('username')
    session_id = data.get('session_id')

    if not username or not session_id:
        return jsonify({'status': 'error', 'message': 'Username and session ID are required'}), 400

    if username not in active_sessions or active_sessions[username] != session_id:
        return jsonify({'status': 'error', 'message': 'Invalid session ID'}), 400

    # Remove the user from active sessions
    del active_sessions[username]

    return jsonify({'status': 'success', 'message': 'Logout successful'})

if __name__ == '__main__':
    app.run(debug=True)
