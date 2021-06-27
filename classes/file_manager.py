import os
import datetime


class FileManager():
    def __init__(self, filepath):
        self.filepath = filepath

    def is_file_empty(self):
        return os.stat(self.filepath).st_size == 0

    def write_data_to_file(self, data: dict):
        with open(self.filepath, 'a') as data_file:
            if not self.is_file_empty():
                data_file.write("\n")

            data_file.write(f"{self.get_current_date()}\n\n")

            for name, value in data.items():
                data_file.write(f"{name}: {value}\n")

            data_file.write("-" * 100)
            data_file.write("\n")

    def get_current_date(self):
        return datetime.datetime.now().isoformat(timespec='seconds', sep=' ')