import json
import re

def get_json_from_llm_response(response):
    # Extract only the JSON
    matches = re.match(r"```json([^`]+)```", response)
    if len(matches.groups()) > 0:
        json_response = matches.group(1)
        return json.loads(json_response)
    else:
        # TODO: Throw errors
        print("No JSON response!")
