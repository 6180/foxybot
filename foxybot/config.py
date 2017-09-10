"""
Load and parse the config file making it 
available to any files that import this.
"""

import json


config = {}

try:
    with open('config.json', 'r') as f:
        config = json.load(f)
except OSError:
    print("Error reading config.json. Make sure the file exists and is readable")
    exit()
