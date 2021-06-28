import requests

from classes.file_manager import FileManager

SWISSBORG_URL = "https://swissborg-api-proxy.swissborg-stage.workers.dev/chsb-v2"

DATA_FILE_PATH = './data/data.txt'


def filter_data_by_key(data: dict, name: str):
    return dict(filter(lambda x: name in x[0], data.items()))


def get_list_of_data():
    """
    returns a list with tuples (the data: dict, the data name: string )
    """
    response = requests.get(SWISSBORG_URL)

    data = response.json()

    chsb_data = filter_data_by_key(data, 'chsb')
    btc_data = filter_data_by_key(data, 'btc')
    eth_data = filter_data_by_key(data, 'eth')
    bnb_data = filter_data_by_key(data, 'bnb')
    usdc_data = filter_data_by_key(data, 'usdc')
    usdt_data = filter_data_by_key(data, 'usdt')

    others_data = dict(
        filter(
            lambda x: not any(word in x[0] for word in [
                'btc', 'usdc', 'usdt', 'chsb', 'transactions', 'eth', 'bnb',
                'SchedulerRunDateTime', 'timestamp'
            ]), data.items()))

    data_list = [
        (chsb_data, "chsb"),
        (btc_data, "btc"),
        (eth_data, "eth"),
        (bnb_data, "bnb"),
        (usdc_data, "usdc"),
        (usdt_data, "usdt"),
        (others_data, "others"),
    ]
    return data_list


def main():

    file_manager = FileManager(filepath=DATA_FILE_PATH)
    file_manager.write_current_date_to_file()

    for tuple_data in get_list_of_data():
        data, name = tuple_data
        file_manager.write_data_to_file(data, name)


if __name__ == "__main__":
    main()
