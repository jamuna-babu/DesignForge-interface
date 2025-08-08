import requests

def get_llm_response(config, prompt):
    url = config.get('llm_url') 
    request_body = {
            "model": config.get('llm_model'),
            "stream": False, 
            "prompt": prompt
    }
    #TODO: Check request-body schema for optimization
    response = requests.post(url, json=request_body)
    llm_response = response.json().get('response')
    return llm_response
