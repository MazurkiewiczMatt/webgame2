import json
import os

# Path to the JSON file that stores character data
CHARACTER_DATA_FILE = '/home/Mazurkiewicz/webgame/webgame2/characters.json'

# Ensure the JSON file exists
if not os.path.exists(CHARACTER_DATA_FILE):
    with open(CHARACTER_DATA_FILE, 'w') as f:
        json.dump({}, f)

# Path to the JSON file that stores user data
USER_DATA_FILE = '/home/Mazurkiewicz/webgame/webgame2/users.json'

# Ensure the JSON file exists
if not os.path.exists(USER_DATA_FILE):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump({}, f)