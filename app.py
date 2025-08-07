from flask import Flask, request
from flask_cors import CORS
from diffusers import StableDiffusionPipeline
import torch
import json
import requests

from model.llm import get_processed_response_from_llm
from schema.request import validate_request_schema
from util import common, pdf_parser, prompt


# ---- CONFIG ----

# TODO: Move this section to a separate file
# load config
config = {}
with open('config.json', 'r') as fp:
    config = json.load(fp)

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

@app.route('/get-all-templates', methods=['GET'])
def get_all_templates():
    """
    Returns all widgets
    """
    pass

@app.route('/get-template-details', methods=['GET'])
def get_template_details():
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
    file = request.files['file']
    pdf_text = pdf_parser.process_pdf(file)
    prompt_text = prompt.generate_prompt(pdf_text) 
    return get_processed_response_from_llm(prompt_text)

@app.route('/llm-json-response', methods=['POST'])
def get_answers():
    """
    Returns JSON-response for LLM prompts specifically designed to contain json-code
    """
    validate_request_schema(request)
    # Extract prompt from payload
    payload = request.json
    prompt = payload["prompt"]
    return get_processed_response_from_llm(prompt)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",)
