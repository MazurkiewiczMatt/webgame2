import json

from .settings import *



def load_characters():
    """Load character data from the JSON file."""
    with open(CHARACTER_DATA_FILE, 'r') as f:
        return json.load(f)

def save_characters(characters):
    """Save character data to the JSON file."""
    with open(CHARACTER_DATA_FILE, 'w') as f:
        json.dump(characters, f)