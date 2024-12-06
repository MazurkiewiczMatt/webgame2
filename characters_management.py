# characters_management.py
import json
from flask import request, jsonify
import os

from authentication import validate_user

# Path to the JSON file that stores character data
CHARACTER_DATA_FILE = 'characters.json'

# Ensure the JSON file exists
if not os.path.exists(CHARACTER_DATA_FILE):
    with open(CHARACTER_DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_characters():
    """Load character data from the JSON file."""
    with open(CHARACTER_DATA_FILE, 'r') as f:
        return json.load(f)

def save_characters(characters):
    """Save character data to the JSON file."""
    with open(CHARACTER_DATA_FILE, 'w') as f:
        json.dump(characters, f)

def character_sheet(active_sessions, characters):
    """Endpoint for getting own character sheet."""
    data = request.get_json()
    username = data.get('username')
    session_id = data.get('session_id')

    validate_user(username, session_id, active_sessions)

    if username not in characters:
        return jsonify({'status': 'error', 'message': 'Character not found'}), 404
    else:
        return jsonify({'status': 'success', 'character': characters.get(username)})

def create_character(active_sessions):
    """Endpoint for creating a new character."""
    data = request.get_json()
    username = data.get('username')
    session_id = data.get('session_id')
    character_data = data.get('character_data')

    validate_user(username, session_id, active_sessions)

    characters = load_characters()

    if username in characters:
        return jsonify({'status': 'error', 'message': 'Character already exists'}), 400

    characters[username] = character_data
    save_characters(characters)

    return jsonify({'status': 'success', 'message': 'Character created successfully'})
