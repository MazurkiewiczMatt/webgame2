# app.py
from flask import Flask, render_template
import threading
import time
from datetime import datetime

from .authentication import signup, login, logout
from .characters_management import character_sheet, create_character, load_characters, save_characters

def update_function():
    characters = load_characters()
    for character in characters:
        if "age" in character:
            character["age"] += 1
        else:
            character["age"] = 1
    save_characters(characters)


def update():
    """Function to execute tasks at every :00, :20, and :40."""
    while True:
        now = datetime.now()
        if now.minute % 1 == 0 and now.second == 0:
            update_function()
            time.sleep(1)  # Prevent multiple executions in the same second
        time.sleep(0.5)  # Check frequently for timing




def create_app(registered_users=None, active_sessions=None):
    app = Flask(__name__, template_folder='/home/Mazurkiewicz/webgame/webgame2/templates/')

    task_thread = threading.Thread(target=update, daemon=True)
    task_thread.start()

    @app.route('/')
    def main_app():
        active_players = list(active_sessions.keys())
        registered_users_list = list(registered_users.keys())
        return render_template('main_page.html', active_players=active_players, registered_users=registered_users_list)

    @app.route('/signup', methods=['POST'])
    def signup_endpoint():
        return signup(registered_users)

    @app.route('/login', methods=['POST'])
    def login_endpoint():
        return login(registered_users, active_sessions)

    @app.route('/logout', methods=['POST'])
    def logout_endpoint():
        return logout(active_sessions)

    @app.route('/character_sheet', methods=['POST'])
    def character_sheet_endpoint():
        return character_sheet(active_sessions)

    @app.route('/create_character', methods=['POST'])
    def create_character_endpoint():
        return create_character(active_sessions)

    return app

