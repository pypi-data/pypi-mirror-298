import base64
from typing import Dict

import requests

from PS3838._utils.constants import URL_PS3838


class Customer():
    def __init__(
        self,
        config: Dict[str, str],
        *args,
        **kwargs
    ):
        self.config = config
        self.base_url = URL_PS3838
        self.auth_header = self._get_auth_header()

    def _get_auth_header(self) -> Dict[str, str]:
        auth_str = f"{self.config['ps3838']['username']}:{self.config['ps3838']['password']}"
        b64_auth_str = base64.b64encode(auth_str.encode('utf-8')).decode('utf-8')
        return {"Authorization": f"Basic {b64_auth_str}", "Content-Type": "application/json"}
    
    def _make_request(
        self, 
        endpoint: str, 
        data: Dict[str, str] = None, 
        params: Dict[str, str] = None, 
        method: str = 'GET'
    ) -> Dict[str, str]:
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.auth_header, params=params)
            elif method == 'POST':
                response = requests.post(url, headers=self.auth_header, json=data)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()  # Try to parse JSON response
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except requests.exceptions.JSONDecodeError as json_err:
            print(f"JSON decode error occurred: {json_err}")
            print(f"Response content: {response.text}")
        
        return {}
    
    def get_balance(self) -> float:
        """
        This function retrieves the balance from the PS3838 API.
        """
        endpoint = "/v1/client/balance"
        return self._make_request(endpoint=endpoint, method='GET')['availableBalance']