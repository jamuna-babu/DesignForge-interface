import json
import re

def extract_json_from_code_block(data):
    json_data = data
    # Extract only the JSON
    matches = re.match(r"```(json)*([^`]+)```", data)
    if matches and len(matches.groups()) > 0:
        json_data = matches.group(2)
    return json.loads(json_data)

def get_key_from_singleton_dict(singleton_dict):
    keys = list(singleton_dict.keys())
    return keys[0]
