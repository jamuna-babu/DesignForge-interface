from flask import Flask, request
from flask_cors import CORS
from diffusers import StableDiffusionPipeline
import torch
import json
import requests
import sqlite3

from model.llm import get_llm_response 
from schema.request import validate_request_schema
from util import pdf_parser
from util.common import get_json_from_llm_response, get_prompt_for_optimized_sd_prompt, get_prompt_for_widget_layout


# ---- CONFIG ----

# TODO: Move this section to a separate file
# load config
config = {}
with open('config.json', 'r') as fp:
    config = json.load(fp)
# initialize DB
connection = sqlite3.connect('database.db')
config['db_connection'] = connection
with open('database/schema.sql') as f:
    connection.executescript(f.read())

app = Flask(__name__)
CORS(app)
# TODO: Check if needed
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB



# ---- ROUTES ----

@app.route('/')
def hello_world():
    """
    Test route
    """
    return 'Hello, World!'

@app.route('/<widget>/save-template', methods=['GET'])
def save_template(widget):
    """
    Returns all widgets
    """
    pass

@app.route('/get-all-templates', methods=['GET'])
def get_all_templates():
    """
    Returns all widgets
    """
    pass

@app.route('/<widget>/get-template-details', methods=['GET'])
def get_template_details(widget):
    """
    Returns layout-JSON for the specified widget
    """
    pass

@app.route('/layout-from-pdf', methods=['POST'])
def parse_pdf():
    """
    Generates widget-layout based on the specifications in the uploaded PDF-file
    """
    validate_request_schema(request)
    file = request.files.get('file')
    pdf_text = pdf_parser.process_pdf(file)
    prompt_text = get_prompt_for_widget_layout(pdf_text) 
    llm_response = get_llm_response(config, prompt_text)
    return get_json_from_llm_response(llm_response)

@app.route('/llm-image-prompt', methods=['POST'])
def get_opt_prompt():
    """
    Returns JSON-response for LLM prompts specifically designed to contain json-code
    """
    validate_request_schema(request)
    # Extract prompt from payload
    payload = request.json
    prompt = payload.get('prompt')
    theme = payload.get('theme')
    llm_response = get_llm_response(config, get_prompt_for_optimized_sd_prompt(theme, prompt))
    return get_json_from_llm_response(llm_response)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",)
