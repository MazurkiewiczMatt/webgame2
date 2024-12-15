# characters_management.py
from flask import request, jsonify

from state_management import load_characters, save_characters

from .authentication import validate_user


def character_sheet(active_sessions):
    """Endpoint for getting own character sheet."""
    data = request.get_json()
    username = data.get('username')
    session_id = data.get('session_id')

    validate_user(username, session_id, active_sessions)

    characters = load_characters()

    if username not in characters:
        return jsonify({'status': 'error', 'message': 'Character not found'}), 404
    else:
        return jsonify({'status': 'success', 'character': characters.get(username)})

def create_character(active_sessions):
    """Endpoint for creating a new character."""
    data = request.get_json()
    username = data.get('username')
    session_id = data.get('session_id')
    starting_point = data.get('starting_point')

    if starting_point not in ("University", "Corporation", "Private Venture"):
        return jsonify({'status': 'error', 'message': f"{starting_point} is not a valid starting point."}), 400

    validate_user(username, session_id, active_sessions)

    characters = load_characters()

    if username in characters:
        return jsonify({'status': 'error', 'message': 'Character already exists'}), 400

    if starting_point == "University":
        ml_expertise = 200
        money = 20000000
        assets = {"University funding": {"price_per_turn": -8000000}}
    elif starting_point == "Corporation":
        ml_expertise = 150
        money = 2000000000
        assets = {}
    elif starting_point == "Private Venture":
        ml_expertise = 0
        money = 200000000
        assets = {"Private funding": {"price_per_turn": -1000000}}

    character = {"starting_point": starting_point,
                 "ml_expertise": ml_expertise,
                 "money": money,
                 "assets": assets}
    characters[username] = character
    save_characters(characters)

    return jsonify({'status': 'success', 'message': 'Character created successfully'})
