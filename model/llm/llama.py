import requests
import json
import re
from flask import abort
from util.common import extract_json_from_code_block,calculate_position_from_json
from util.widget import WidgetLayout

class Llama:
    def __init__(self, config):
        self.config = config.get('llama')

    def get_and_process_llm_response(self, prompt):
        url = self.config.get('url') 
        request_body = {
                "model": self.config.get('model'),
                "stream": False, 
                "prompt": prompt
        }
        print(url)
        #TODO: Check request-body schema for optimization
        response = requests.post(url, json=request_body)
        llm_response = response.json().get('response')
        return self.process_llm_response(llm_response) 
        
    
    # def process_llm_response(self, response_data):
    #     print(response_data,"response_data")
    #     # json_data = extract_json_from_code_block(response_data) # Now it's a dictionary
    #     # self.validate_llm_json(json_data)
    #     # create widget-layout
    #     # widget_layout = WidgetLayout(json_data)
    #     # return widget_layout.construct_complete_layout()
        
    #     value= calculate_position_from_json(json.loads(response_data))
    #     print(value)
    #     return value

    def validate_llm_json(self, data):
        for key in ['widget_name', 'device_type']:
            if not data.get(key, None):
                abort(415, f"{key} not found!")
        for key in ['overall_width', 'overall_height']:
            if not data.get(key, None):
                abort(415, "Guidelines is not as per set standards!")

    
        # More validations are made during construction of widget-layout
    import json

    def process_llm_response(self, response_data):
        print("RAW:", repr(response_data))

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
