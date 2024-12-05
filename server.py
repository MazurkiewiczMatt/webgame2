from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

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

    return jsonify({'status': 'success', 'message': 'Login successful'})

if __name__ == '__main__':
    app.run(debug=True)
