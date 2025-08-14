import requests

# TODO: Convert to class
def get_processed_image(config, params):
    url = config.get('stable_diffusion').get('url') 
    request_body = {
            "prompt": params.get('prompt'),
            "width": params.get('width'),
            "height": params.get('height')
    }
    print(url,request_body,"url and request body")
    #TODO: Check request-body schema for optimization
    response = requests.post(url, json=request_body)
    sd_response = response.json()
    return sd_response 
