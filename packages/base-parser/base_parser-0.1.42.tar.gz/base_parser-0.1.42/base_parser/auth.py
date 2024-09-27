import base64
from .utils import (
    default_source_headers,
    check_connection
)
import requests
from typing import Optional
from .log.logger import Logger
from .config_parser.config import Config


class Auth:

    def __init__(self,
                 config: Config,
                 auth_url,
                 auth_type,
                 *,
                 api_key='api_key',
                 key_name='key_name',
                 auth_endpoint='/'):
        self.config = config
        self.auth_url = auth_url
        self.auth_type = auth_type
        self.auth_header = None
        self.refresh_token = None

        match self.auth_type:
            case "1":
                pass  # todo
            case "2":
                self.api_key(api_key, key_name)
            case "3":
                self.basic_auth()
            case "4":
                check_connection(url=auth_url, endpoint=auth_endpoint)
                self.login_pass_auth()
            case "5":
                self.set_constant_auth_token(api_key)
            case _:
                pass  # todo

    def login_pass_auth(self):
        auth_password = self.config.get_features_auth_password()
        auth_username = self.config.get_features_auth_username()
        h = Logger()
        auth_creds = {
            "password": auth_password,
            "username": auth_username
        }
        try:
            response = requests.post(self.auth_url, headers=default_source_headers, json=auth_creds, verify=False)
            if response.status_code == 200:
                access_token = response.json().get('access_token')
                self.auth_header = {'Authorization': f'Bearer {access_token}'}
                self.refresh_token = response.json().get('refresh_token')
            else:
                raise Exception(f"Failed to obtain access token: {response.status_code} {response.text}")

        except Exception as error:
            h.Error("Error in sending auth message: " + error.__str__())

    def basic_auth(self):
        auth_password = self.config.get_features_auth_password()
        auth_username = self.config.get_features_auth_username()
        auth_string = f"{auth_username}:{auth_password}"
        base64_auth_string = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')
        self.auth_header = {'Authorization': f'Basic {base64_auth_string}'}

    def oauth2(self, token_url: str, client_id: str, client_secret: str, scope: Optional[str] = None):
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        }
        if scope:
            data['scope'] = scope

        response = requests.post(token_url, data=data)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            self.auth_header = {'Authorization': f'Bearer {access_token}'}
        else:
            raise Exception(f"Failed to obtain access token: {response.status_code} {response.text}")

    def bearer_token(self, token: str):
        self.auth_header = {'Authorization': f'Bearer {token}'}

    def api_key(self, key_name: str, api_key: str):
        self.auth_header = {key_name: api_key}

    def get_auth_header(self):
        if not self.auth_header:
            raise ValueError("Authentication method is not set.")
        return self.auth_header

    def set_constant_auth_token(self, token):
        self.auth_header = {"Authorization": token}
