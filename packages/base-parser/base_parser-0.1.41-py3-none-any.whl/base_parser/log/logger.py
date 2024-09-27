import datetime
import os


class Logger:
    def __init__(self, log_file='log/logs.txt'):
        self.log_file = log_file
        self._ensure_log_file_exists()

    def _ensure_log_file_exists(self):
        log_directory = os.path.dirname(self.log_file)

        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as file:
                file.write("Log file created.\n")

    def _write_log(self, level, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"{timestamp} [{level}] {message}\n"

        with open(self.log_file, 'a') as file:
            file.write(log_message)

    def Error(self, message):
        self._write_log('ERROR', message)

    def Info(self, message):
        self._write_log('INFO', message)

    def Debug(self, message):
        self._write_log('DEBUG', message)
