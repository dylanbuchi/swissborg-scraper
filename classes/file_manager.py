import os
import datetime

from io import TextIOWrapper


class FileManager():
    def __init__(self, filepath):
        self.filepath = filepath
        self.folder_name = self.get_folder_name()
        self.filename = self.get_filename()
        self.check_path_exists()

    def is_file_empty(self):
        return os.stat(self.filepath).st_size == 0

    def write_data_to_file(self, data: dict):
        with open(self.filepath, 'a') as data_file:
            if not self.is_file_empty():
                data_file.write("\n")

            self._write_current_date_to_file(data_file)

            for name, value in data.items():
                data_file.write(f"{name}: {value}\n")

            self._draw_a_line(file=data_file, line_length=100)
            self._write_new_line(data_file)

    def get_current_date(self):
        return datetime.datetime.now().isoformat(timespec='seconds', sep=' ')

    def _write_current_date_to_file(self, file: TextIOWrapper):
        file.write((f"{self.get_current_date()}\n\n"))

    def _draw_a_line(self, file: TextIOWrapper, line_length: int):
        file.write("-" * line_length)

    def _write_new_line(self, file: TextIOWrapper):
        file.write("\n")

    def _get_negative_index_to_get_name_from(self, path):
        index = path[::-1].find("/")

        return -index

    def get_filename(self):
        index = self._get_negative_index_to_get_name_from(self.filepath)
        if self.folder_name == './' or index == 0:
            return ''
        else:
            return self.filepath[index:]

    def get_folder_name(self):
        folder_path = str(os.path.dirname(self.filepath))

        if (folder_path == '.'):
            return './'
        else:
            index = self._get_negative_index_to_get_name_from(folder_path)
            return folder_path[index:]

    def check_path_exists(self):
        if not os.path.exists(self.filepath) or self.filename == '':
            raise FileNotFoundError()
        return True


if __name__ == "__main__":
    ...