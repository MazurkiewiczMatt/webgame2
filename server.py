import sys

from server_app import create_app
from state_management import load_users

# Add your specific path if needed for importing
path = '/home/Mazurkiewicz/webgame/webgame2'
if path not in sys.path:
    sys.path.append(path)

registered_users = load_users()
active_sessions = {}


app = create_app(registered_users=registered_users,
                 active_sessions=active_sessions)
