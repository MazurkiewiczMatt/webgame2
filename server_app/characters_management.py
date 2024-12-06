# characters_management.py
from flask import request, jsonify

from state_management import load_characters, save_characters

from .authentication import validate_user


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
