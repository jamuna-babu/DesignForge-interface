import requests
import json
import re
from flask import abort
from util.common import extract_json_from_code_block

class Gemma:
    def __init__(self, config):
        self.config = config.get('gemma')

    def get_and_process_llm_response(self, prompt):
        url = self.config.get('url') 
        request_body = {
                "model": self.config.get('model'),
                "stream": False, 
                "prompt": prompt
        }
        #TODO: Check request-body schema for optimization
        response = requests.post(url, json=request_body)
        llm_response = response.json().get('response')
        return self.process_llm_response(llm_response) 

    def process_llm_response(self, response):
        return extract_json_from_code_block(response)

