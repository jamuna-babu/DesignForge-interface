import requests
from util.common import get_json_from_llm_response

def get_processed_response_from_llm(config, prompt):
    url = f"http://{config.get('ip')}:11434/api/generate"
    response = requests.post(url, json={"model": "gemma3:4b", "stream": False, "prompt": prompt})
    llm_response = response.json().get('response')
    return get_json_from_llm_response(llm_response)
