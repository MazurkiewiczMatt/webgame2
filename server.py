# server.py
from flask import Flask, request, jsonify, render_template
import sys
import authentication
import characters_management

app = Flask(__name__, template_folder='/home/Mazurkiewicz/webgame/webgame2/templates/')

# Add your specific path if needed for importing
path = '/home/Mazurkiewicz/webgame/webgame2'
if path not in sys.path:
    sys.path.append(path)

# Dictionary to hold active users with session IDs
active_sessions = {}
characters = characters.load_characters()

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

if __name__ == '__main__':
    app.run(debug=True)
