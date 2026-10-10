import requests
import json
import re
from flask import abort
from util.common import extract_json_from_code_block,calculate_position_from_json

class Gemma:
    def __init__(self, config):
        self.config = config.get('gemma')

    def get_and_process_llm_response(self, prompt):
        url = self.config.get('url') 
        print(url,"url")
        request_body = {
                "model": self.config.get('model'),
                "stream": False, 
                "prompt": prompt
        }
        print(request_body,"request")
        #TODO: Check request-body schema for optimization
        response = requests.post(url, json=request_body)
        llm_response = response.json().get('response')
        return self.process_llm_response(llm_response) 

    def process_llm_response(self, response_data):

        print("RAW:", response_data,"from meeeeeeeeeeee")

        # If already dict, no need to parse
        if isinstance(response_data, dict):
            json_data = response_data
        else:
            # Clean code fences if AI added them
            if response_data.strip().startswith("```"):
                response_data = "\n".join(
                    line for line in response_data.splitlines() if not line.strip().startswith("```")
                )

            try:
                json_data = json.loads(response_data)
            except json.JSONDecodeError as e:
                print("JSON decode failed:", e)
                return None  # or raise

        value = calculate_position_from_json(json_data)
        print("Value:", value)
        return value

    

