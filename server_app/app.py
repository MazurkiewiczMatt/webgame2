# app.py
from flask import Flask, render_template
import threading
from datetime import datetime, timedelta

from .authentication import signup, login, logout
from .characters_management import character_sheet, create_character, load_characters, save_characters

def update_function():
    characters = load_characters()
    for character in characters.keys():
        if "age" in characters[character].keys():
            characters[character]["age"] += 1
        else:
            characters[character]["age"] = 1
    save_characters(characters)
    schedule_next_update()



def schedule_next_update():
    now = datetime.now()
    next_run = (now + timedelta(minutes=1)).replace(second=0, microsecond=0)
    delay = (next_run - now).total_seconds()
    threading.Timer(delay, update_function).start()




def create_app(registered_users=None, active_sessions=None):
    app = Flask(__name__, template_folder='/home/Mazurkiewicz/webgame/webgame2/templates/')

    update_function()

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

