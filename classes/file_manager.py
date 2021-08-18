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

    def write_data_to_file(self, data: dict, title: str):
        with open(self.filepath, 'a') as data_file:
            if not self.is_file_empty():
                self._write_new_line(data_file)

            self._write_new_line(data_file)

            data_file.write(f"{title.upper()}:\n\n")

            for name, value in data.items():
                name = self._upper_first_word(
                    self._camel_case_to_human_readable(name))
                value = self._set_correct_data_values(name, value)

                data_file.write(f"{name}: {value}\n")

            self._draw_line(file=data_file, line_length=100)
            self._write_new_line(data_file)

    def get_current_date(self):
        return datetime.datetime.now().isoformat(timespec='seconds', sep=' ')

    def write_current_date_to_file(self):
        with open(self.filepath, 'a') as data_file:
            data_file.write((f"{self.get_current_date()}\n\n"))

    def _draw_line(self, file: TextIOWrapper, line_length: int):
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
        index = self._get_negative_index_to_get_name_from(folder_path)
        return folder_path[index:]

    def check_path_exists(self):
        if not os.path.exists(self.filepath) or self.filename == '':
            raise FileNotFoundError()
        return True

    def _camel_case_to_human_readable(self, string: str):
        result = []

        index = 0

        while (index < len(string)):
            if string[index].isupper():
                upper_letters = []
                result.append(" ")
                while (index < len(string) and string[index].isupper()):
                    upper_letters.append(string[index])
                    index += 1
                result.append(''.join(upper_letters))
            else:
                result.append(string[index])
                index += 1

        return ''.join(result).title()

    def _set_correct_data_values(self, name: str, value: str):

        value = self.replace_trailing_zeros_from(f"{float(value):,.2f}")

        if "percentage" in name.lower():
            return f"{value}%"
        else:
            return value

    def _upper_first_word(self, string: str):
        parts = string.split()
        if len(parts[0]) < 5:
            parts[0] = parts[0].upper()
        return ' '.join(parts)

    def replace_trailing_zeros_from(self, string: str):
        if '.00' in string[-3:]:
            string = string.replace('.00', '')
        return string
