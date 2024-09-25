import json
import re
import yaml
import argparse


class Config:
    """
    Class to work with *.yaml files.

    Contains 2 possible method patterns:

    load_*  -   Loading methods - returning dicts of config templates

    get_*   -   Get method - get value of any possible field
    """
    config = None

    def __init__(self, file_path):
        self.file_path = file_path

    def load_json_template(self):
        return self.config.get("json_template")

    def load_endpoint_templates(self):
        return self._find_endpoint_values_recursive(self.config)

    def load_receiver_template(self):
        return self.config.get("receiver")

    def load_yaml_config(self):
        with open(self.file_path, 'r') as file:
            try:
                self.config = yaml.load(file, Loader=yaml.FullLoader)
            except yaml.YAMLError as exc:
                print(f"Ошибка при чтении YAML файла: {exc}")
                return None

    def load_json_config(self):
        with open(self.file_path, 'r') as file:
            try:
                self.config = json.load(file)
            except json.JSONDecodeError as exc:
                print(f"Ошибка при чтении JSON файла: {exc}")
                return None

    def get_source_source(self):
        return self.config['source']['host']

    def get_source_port(self):
        return self.config['source']['port']

    def get_source_type(self):
        return self.config['source']['type']

    def get_source_files_dir(self):
        return self.config['source']['files_dir']

    def get_receiver_send_limit(self):
        return self.config["receiver"]["send_limit"]

    def get_evasion_proxy(self):
        return self.config['evasion']['proxy']

    def get_evasion_vpn(self):
        return self.config['evasion']['vpn']

    def get_evasion_robots(self):
        return self.config['evasion']['robots']

    def get_evasion_sleep(self):
        return self.config['evasion']['sleep']

    def get_evasion_captcha(self):
        return self.config['evasion']['captcha']

    def get_evasion_time(self):
        return self.config["evasion"]["sleep"]

    def load_features_template(self):
        return self.config.get("features")

    def get_features_auth_type(self):
        return self.load_features_template()['auth']['type']

    def get_features_auth_url(self):
        return self.load_features_template()['auth']['url']

    def get_features_auth_password(self):
        return self.load_features_template()['auth']['password']

    def get_features_auth_username(self):
        return self.load_features_template()['auth']['username']

    def get_endpoint_sources(self):
        endpoint_sources = []

        data = self.load_endpoint_templates()
        for endp in data:
            source = endp.get("source")
            endpoint_sources.append(source)
        return endpoint_sources

    def get_endpoint_attr_name(self, curr_endpoint_template):
        return curr_endpoint_template.get("attr")['value']

    def get_relation_field(self, curr_endpoint_template):
        return curr_endpoint_template.get('relation')['value']

    def get_endpoints_attr_names(self):
        data = []
        for i in range(self.load_endpoint_templates().__len__()):
            data.append(self.load_endpoint_templates()[i])
        return data

    def get_endpoint_fields(self, dict: dict):
        return dict.get("fields")

    def get_endpoint_limit(self):
        for i in range(self.load_endpoint_templates().__len__()):
            data = self.load_endpoint_templates()[i]
            try:
                return data.get("limit")['value']
            except Exception as e:
                return e

    def get_endpoint_filters(self):
        for i in range(self.load_endpoint_templates().__len__()):
            data = self.load_endpoint_templates()[i]
            try:
                return data.get("filter")['value']
            except Exception as e:
                return e

    def get_json_parser_source(self):
        return self.load_json_template().get("parser_source")['value']

    def get_receiver_url(self):
        return self.config["receiver"]["url"]

    def get_receiver_api_token(self):
        return self.config["receiver"]["auth"]["token"]

    def get_receiver_auth_type(self):
        return self.config["receiver"]["auth"]["type"]

    def get_curr_endpoint_source(self, curr_endpoint):
        return curr_endpoint.get("source")['value']

    def get_curr_endpoint_filter(self, curr_endpoint):
        return curr_endpoint.get("filter")['value']

    def split_string_by_multiple_delimiters(self, delimiters: str, string: str) -> list:
        result = re.split(delimiters, string)
        return [item for item in result if item]

    def _find_endpoint_values_recursive(self, data):
        endpoint_values = []

        if isinstance(data, dict):
            for key, value in data.items():
                if key.startswith("endpoint"):
                    endpoint_values.append(value)
                elif isinstance(value, dict) or isinstance(value, list):
                    endpoint_values.extend(self._find_endpoint_values_recursive(value))

        elif isinstance(data, list):
            for item in data:
                endpoint_values.extend(self._find_endpoint_values_recursive(item))

        return endpoint_values


def parse_args():
    parser = argparse.ArgumentParser(description='Парсинг конфигурационного файла YAML.')
    parser.add_argument('config_path', type=str, help='Путь к YAML файлу конфигурации.')
    return parser.parse_args()


def main():
    args = parse_args()
    config_path = args.config_path
    cnf = Config(config_path)
    cnf.load_yaml_config()
    print(cnf.config)


if __name__ == '__main__':
    main()
