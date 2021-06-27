import requests
import os
import datetime

from bs4 import BeautifulSoup

SWISSBORG_URL = "https://swissborg.com/chsb-overview"

CHSB_CIRCULATING_SUPPLY_DATA_FILE_PATH = './data/chsb_circulating_supply_data.txt'


def get_current_date():
    return datetime.datetime.now().isoformat(timespec='seconds', sep=' ')


def get_chsb_circulating_supply_data():
    """
    returns a dict with the 4 items from H2: "A breakdown of CHSB circulating supply" part of the chsb overview page
    """
    response = requests.get(SWISSBORG_URL)
    soup = BeautifulSoup(response.content, features="html.parser")

    div_container_name = "unwzr5-0 gOLdjf"
    div_containers = soup.find_all("div", class_=div_container_name)

    data = {}

    for div in div_containers:
        p_list = div.find_all("p")

        if len(p_list) > 2:
            value, value_description, name = p_list
            long_value = f"{value.text} {value_description.text}"

            data[name.text] = long_value
        else:
            value, name = p_list
            data[name.text] = value.text

    return data


def write_data_to_file(filepath: str, data: dict):
    with open(filepath, 'a') as data_file:
        if not os.stat(filepath).st_size == 0:
            data_file.write("\n")
        data_file.write(f"{get_current_date()}\n\n")

        for name, value in data.items():
            data_file.write(f"{name}: {value}\n")

        data_file.write("-" * 100)
        data_file.write("\n")


def main():
    chsb_circulating_supply_data = get_chsb_circulating_supply_data()

    write_data_to_file(CHSB_CIRCULATING_SUPPLY_DATA_FILE_PATH,
                       chsb_circulating_supply_data)


if __name__ == "__main__":
    main()
