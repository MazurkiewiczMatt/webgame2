# app.py
from flask import Flask, render_template

from .authentication import signup, login, logout
from .characters_management import character_sheet

from state_management import load_users


def create_app(registered_users=None, active_sessions=None, character_sheets=None):
    app = Flask(__name__, template_folder='/home/Mazurkiewicz/webgame/webgame2/templates/')

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
        return character_sheet(active_sessions, character_sheets)

    return app


if __name__ == '__main__':
    # Initialize the app with default active sessions and characters
    app = create_app()
    app.run(debug=True)