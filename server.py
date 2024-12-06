import sys

from server import create_app, load_characters

# Add your specific path if needed for importing
path = '/home/Mazurkiewicz/webgame/webgame2'
if path not in sys.path:
    sys.path.append(path)

if __name__ == '__main__':
    active_sessions = {}
    characters = load_characters()
    app = create_app(active_sessions=active_sessions, characters=characters)
    app.run(debug=True)