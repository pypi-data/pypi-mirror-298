import requests
import logging

class APIClient:
    def __init__(self, base_url, api_key, email):
        # Check if the base URL matches the specified user-facing URL
        if base_url == 'https://api.fotographer.ai/Image-gen':
            # Use the cloud function URL instead
            self.base_url = 'https://asia-northeast1-moon-61b6f.cloudfunctions.net/Image-gen'
        else:
            # Use the provided base URL
            self.base_url = base_url
        
        self.api_key = api_key
        self.email = email
        logging.basicConfig(level=logging.DEBUG)

    def post(self, endpoint, json_data=None, timeout=120):
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': self.api_key,
            'x-email': self.email
        }
        url = f'{self.base_url}/{endpoint}'
        try:
            response = requests.post(url, headers=headers, json=json_data, timeout=timeout)
            response.raise_for_status()
            logging.debug(f'Response: {response.status_code} {response.text}')
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f'HTTP error occurred: {http_err}')
            logging.error(f'Response content: {response.content}')
            raise
        except Exception as err:
            logging.error(f'Other error occurred: {err}')
            raise
