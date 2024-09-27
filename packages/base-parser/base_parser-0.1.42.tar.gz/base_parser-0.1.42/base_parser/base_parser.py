import json
import tarfile
import zipfile
from abc import ABC, abstractmethod
import requests
import os
from .config_parser import config
from .log.logger import Logger
from .auth import Auth
from .utils import default_api_headers, default_source_headers, check_path


class Parser(ABC):

    def __init__(self, cnf: config.Config):
        self.cnf = cnf
        self.offset = 0  # used for scrolling vulns in response
        self.limit = None  # used for limiting number of vulns in one response
        self.api_headers = default_api_headers  # headers for receiver API
        self.source_headers = default_source_headers  # headers for source

    @abstractmethod
    async def parse(self):
        pass

    async def download_file(self, url, dir: str = "downloaded_files"):
        '''
                Метод для скачивания любого файла по ссылке
        '''

        # Создаем директорию, если она не существует
        check_path(dir)

        # Имя файла, который мы будем скачивать
        local_filename = os.path.join(dir, url.split('/')[-1])

        # Скачиваем файл
        with requests.get(url, stream=True) as response:
            if response.status_code == 200:
                with open(local_filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Файл {local_filename} скачан.")
            else:
                print(f"Ошибка при скачивании файла: {response.status_code}")
                return

        # Проверка, является ли файл архивом ZIP
        if zipfile.is_zipfile(local_filename):
            with zipfile.ZipFile(local_filename, 'r') as zip_ref:
                zip_ref.extractall(dir)
            print(f"Архив {local_filename} успешно распакован в {dir}.")

        # Проверка, является ли файл архивом TAR
        elif tarfile.is_tarfile(local_filename):
            with tarfile.open(local_filename, 'r') as tar_ref:
                tar_ref.extractall(dir)
            print(f"Архив {local_filename} успешно распакован в {dir}.")

        else:
            print(f"Файл {local_filename} не является архивом.")

    @abstractmethod
    async def get_data(self, *args):
        pass

    async def validate(self):
        pass
        #todo

    @abstractmethod
    async def fetch_before_send(self, vulns_to_send):
        '''
                Метод для финальных точечных правок в поля конкретной уязвимости перед отправкой в базу

                :param vulns_to_send:
                :return vulns_refactored:
        '''
        pass

    async def send_to_receiver(self, vulns_to_send):
        h = Logger()
        try:
            auth = Auth(
                self.cnf,
                self.cnf.get_receiver_url(),
                self.cnf.get_receiver_auth_type(),
                api_key=self.cnf.get_receiver_api_token()
            )
            if auth.auth_header is not None:
                h.Info("Authenticated successfully")
                self.api_headers.update(auth.get_auth_header())
            else:
                h.Info("Continuing without authentication header...")
        except Exception as e:
            h.Error(f"Failed to authenticate: {e.__str__()}")

        json_to_send = self.fetch_before_send(vulns_to_send)
        jsons_to_send = {"vulnerabilities": json_to_send}
        r = requests.post(self.cnf.get_receiver_url(),
                          json.dumps(jsons_to_send, indent=4, ensure_ascii=False), verify=False, headers=
                          self.api_headers)
        if r.status_code == 201:
            h.Info(f"Vulnerabilities sent successfully")
        else:
            h.Error(f"Vulns were not sent due to error. HTTP code: {r.status_code}")
            if r:
                h.Error(f"Message: {r}")
            h.Debug(f"Json which was sended: {json.dumps(jsons_to_send, indent=4, ensure_ascii=False)}")
            h.Debug(f"Request URL: {self.cnf.get_receiver_url()}")
            h.Debug(f"Request headers: {self.api_headers}")

