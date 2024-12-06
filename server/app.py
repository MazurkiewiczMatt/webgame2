# server.py
from flask import Flask, render_template
import authentication, characters_management


def create_app(active_sessions=None, characters=None):
    app = Flask(__name__, template_folder='/home/Mazurkiewicz/webgame/webgame2/templates/')

    # Set default references if none provided


    @app.route('/')
    def main_app():
        active_players = list(active_sessions.keys())
        registered_users = list(authentication.load_users().keys())
        return render_template('main_page.html', active_players=active_players, registered_users=registered_users)

    @app.route('/signup', methods=['POST'])
    def signup():
        return authentication.signup()

    @app.route('/login', methods=['POST'])
    def login():
        return authentication.login(active_sessions)

    @app.route('/logout', methods=['POST'])
    def logout():
        return authentication.logout(active_sessions)

    @app.route('/character_sheet', methods=['POST'])
    def character_sheet():
        return characters_management.character_sheet(active_sessions, characters)

    return app


if __name__ == '__main__':
    # Initialize the app with default active sessions and characters
    app = create_app()
    app.run(debug=True)
