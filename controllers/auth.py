import requests

def call_other_service(api_url, jwt_token):
    headers = {
        'Authorization': f'Bearer {jwt_token}'
    }
    response = requests.get(api_url, headers=headers)
    return response.json()