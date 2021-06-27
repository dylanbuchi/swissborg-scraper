import requests
import os

from classes.file_manager import FileManager

from bs4 import BeautifulSoup

SWISSBORG_URL = "https://swissborg.com/chsb-overview"

CHSB_CIRCULATING_SUPPLY_DATA_FILE_PATH = './data/chsb_circulating_supply_data.txt'


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


def main():
    file_manager = FileManager(filepath=CHSB_CIRCULATING_SUPPLY_DATA_FILE_PATH)

    chsb_circulating_supply_data = get_chsb_circulating_supply_data()
    file_manager.write_data_to_file(chsb_circulating_supply_data)


if __name__ == "__main__":
    main()
