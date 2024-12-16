import sys
import threading
import time
from datetime import datetime

from server_app import create_app
from state_management import load_characters, load_users

# Add your specific path if needed for importing
path = '/home/Mazurkiewicz/webgame/webgame2'
if path not in sys.path:
    sys.path.append(path)

registered_users = load_users()
active_sessions = {}
character_sheets = load_characters()


def my_function():
    """Your custom function to execute."""
    print("Executing my scheduled task!")


def update():
    """Function to execute tasks at every :00, :20, and :40."""
    while True:
        now = datetime.now()
        if now.minute % 1 == 0 and now.second == 0:
            print(f"Update executed at {now}")
            # Call your desired function here
            my_function()
            time.sleep(1)  # Prevent multiple executions in the same second
        time.sleep(0.5)  # Check frequently for timing


task_thread = threading.Thread(target=update, daemon=True)
task_thread.start()

app = create_app(registered_users=registered_users,
                 active_sessions=active_sessions,
                 character_sheets=character_sheets)
