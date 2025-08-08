import requests
from util.common import get_json_from_llm_response

def get_processed_image(config, params):
    url = config.get('stable_diffusion_url') 
    request_body = {
            "prompt": params.get('prompt'),
            "width": params.get('width'),
            "height": params.get('height')
    }
    #TODO: Check request-body schema for optimization
    response = requests.post(url, json=request_body)
    print(response)
    sd_response = response.json()
    return sd_response 
