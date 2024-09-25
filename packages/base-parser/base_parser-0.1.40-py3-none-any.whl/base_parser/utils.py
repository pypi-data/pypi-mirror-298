import os
from .log.logger import Logger
import requests

default_api_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'uk,en-US;q=0.9,en;q=0.8,ru;q=0.7',
    'sec-ch-ua': '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    "Content-Type": "application/json"
}

default_source_headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'uk,en-US;q=0.9,en;q=0.8,ru;q=0.7',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    "Content-Type": "application/json"
}


def check_path(file_path: str) -> bool:
    h = Logger()
    if os.path.exists(file_path):
        return True
    else:
        h.Error(f"Provided path does not exist: {file_path}")
        return False


def validate_json_structure(data, required_structure):
    if isinstance(data, dict) and isinstance(required_structure, dict):
        for key, value in required_structure.items():
            if key not in data:
                print(f"Missing key: {key}")
                return False
            if not validate_json_structure(data[key], value):
                print(f"Invalid structure at key: {key}")
                return False
    elif isinstance(data, list) and isinstance(required_structure, list) and required_structure:
        for item in data:
            if not validate_json_structure(item, required_structure[0]):
                return False
    return True


def check_connection(url: str = 'url', endpoint: str = 'endpoint') -> bool:
    h = Logger()
    if endpoint:
        full_url = f"{url.rstrip('/')}/{endpoint.lstrip('/')}"
    else:
        full_url = f"{url.rstrip('/')}"
    try:
        response = requests.get(full_url, headers=default_source_headers, timeout=5, verify=False)
        if 200 <= response.status_code < 300:
            return True
        else:
            h.Info(f"Test connection: Specified address responded with status code: {response.status_code}")
            return False
    except requests.ConnectionError:
        h.Info("Test connection: Failed to connect to the server.")
        return False
    except requests.Timeout:
        h.Info("Test connection: The request timed out.")
        return False
    except requests.RequestException as e:
        h.Info(f"Test connection: An error occurred connecting to {full_url}. {e}")
        return False