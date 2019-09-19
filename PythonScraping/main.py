import argparse
from typing import Dict


def get_search_text_args() -> str:
    """
    Gets a string
    :return: The string
    """
    parser = argparse.ArgumentParser(description='Gets a string representing a text')
    parser.add_argument('-t', '--text', type=str, required=True, help="The word that you want to search for.")
    args = parser.parse_args()
    return args.text


def print_modules_example(modules_example: Dict) -> None:
    """
    Prints the module-example pairs
    :param modules_example: A dict containing module-example pairs
    :return: -
    """
    for key, val in modules_example.items():
        print(key, 'Example:\n', val, '\n')
