from flask import Flask, request, abort
from flask_cors import CORS
import json
import sqlite3

from model.llm import gemma, llama 
from model.stable_diffusion import get_processed_image
from schema.request import validate_request_schema
from template.accessor import TemplateAccessor
from util import pdf_parser
from prompts import llama_layout, gemma_layout, gemma_image_prompt


# ---- CONFIG ----

# TODO: Move this section to a separate file
# load config
config = {}
with open('config.json', 'r') as fp:
    config = json.load(fp)
# initialize DB
connection = sqlite3.connect('database.db', check_same_thread=False)
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

@app.route('/save-template', methods=['POST'])
def save_template():
    """
    Save the layout of the device's widget to DB
    The layout schema is as follows
    { 
      "[widget]": {
        "[device]": {},
      }
    } 
    """
    payload = request.json
    try:
        template_accessor = TemplateAccessor(connection)
        template_accessor.save_template(payload)
        return { "is_successful": True }
    except Exception as e:
        print(e)
        return abort(500, "Template could not be saved")

@app.route('/get-all-templates', methods=['GET'])
def get_all_templates():
    """
    Returns all widgets in the following format
    { 
      "[widget_1]": {
        "[device_1]": {},
        "[device_2]": {},
        "[device_3]": {},
      },
      "[widget_2]": {
        "[device_1]": {},
        "[device_2]": {},
        "[device_3]": {},
      },
    } 
    """
    try:
        template_accessor = TemplateAccessor(connection)
        return template_accessor.get_all_templates()
    except Exception as e:
        print(e)
        return abort(500, "Error retrieving templates")

@app.route('/layout-from-pdf/<version>', methods=['POST'])
def parse_pdf(version):
    """
    Generates widget-layout based on the specifications in the uploaded PDF-file
    """
    validate_request_schema(request)
    file = request.files.get('file')
    # get text from pdf
    pdf_text = pdf_parser.process_pdf(file)
    # set model based on the 'version' parameter
    prompt_generator = None
    model = None
    if version == 'v1':
        # Use Gemma
        prompt_generator = gemma_layout.generate_prompt
        model = gemma.Gemma(config)
    else:
        # Use Llama
        prompt_generator = llama_layout.generate_prompt
        model = llama.Llama(config)
        pass
    # generate prompt
    prompt_text = prompt_generator(pdf_text)
    # get and process response from model
    processed_response = model.get_and_process_llm_response(prompt_text) 
    return processed_response

@app.route('/llm-image-prompt', methods=['POST'])
def get_optimized_prompt():
    """
    Returns JSON-response for LLM prompts specifically designed to contain json-code
    (Designed to work with Gemma only)
    """
    validate_request_schema(request)
    payload = request.json
    # generate prompt
    prompt_text = gemma_image_prompt.generate_prompt(payload)
    model = gemma.Gemma(config)
    # get and process response from model
    processed_response = model.get_and_process_llm_response(prompt_text) 
    return processed_response

@app.route('/sd-image-gen', methods=['POST'])
def get_image():
    validate_request_schema(request)
    payload = request.json
    # TODO: Use object
    return get_processed_image(config, payload)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0",)
