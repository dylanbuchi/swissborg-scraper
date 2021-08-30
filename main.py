import requests

from classes.file_manager import FileManager
from classes.crypto import Crypto

SWISSBORG_URL = "https://swissborg-api-proxy.swissborg-stage.workers.dev/chsb-v2"

DATA_FILE_PATH = './data/data.txt'


def filter_data_by_key(data: dict, name: str):
    return dict(filter(lambda x: name in x[0], data.items()))


def create_data_list_from(data: dict):
    data_names = Crypto.crypto_names_list
    exclude_items = ['transactions', 'SchedulerRunDateTime', 'timestamp']

    data_list = [(filter_data_by_key(data, name), name) for name in data_names]

    others_data = dict(
        filter(
            lambda x: all(word not in x[0]
                          for word in data_names + exclude_items),
            data.items(),
        ))

    data_list.append((others_data, "others"))
    return data_list


def get_list_of_data():
    """
    returns a list with tuples (the data: dict, the data name: string )
    """
    response = requests.get(SWISSBORG_URL)

    data = response.json()

    return create_data_list_from(data)


def main():

    file_manager = FileManager(filepath=DATA_FILE_PATH)
    file_manager.write_current_date_to_file()

    for tuple_data in get_list_of_data():
        data, name = tuple_data
        file_manager.write_data_to_file(data, name)


if __name__ == "__main__":
    main()
