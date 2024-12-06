import json
import os

# Path to the JSON file that stores character data
CHARACTER_DATA_FILE = 'characters.json'

# Ensure the JSON file exists
if not os.path.exists(CHARACTER_DATA_FILE):
    with open(CHARACTER_DATA_FILE, 'w') as f:
        json.dump({}, f)

def load_characters():
    """Load character data from the JSON file."""
    with open(CHARACTER_DATA_FILE, 'r') as f:
        return json.load(f)

def save_characters(characters):
    """Save character data to the JSON file."""
    with open(CHARACTER_DATA_FILE, 'w') as f:
        json.dump(characters, f)