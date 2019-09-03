import argparse
import sys

from typing import List
import requests
from bs4 import BeautifulSoup

from PUBG.bsoup import continents_list, countries_list, players_list
from PUBG.alchemy import *


def insert_continents() -> None:
    s = 'https://liquipedia.net/pubg/Portal:Players'
    source = requests.get(s).text
    soup = BeautifulSoup(source, 'html.parser')

    continents = continents_list(soup)
    add_continents(continents)


def insert_countries_from_continent(continent: str) -> None:
    s = 'https://liquipedia.net/pubg/Portal:Players/' + continent
    source = requests.get(s).text
    soup = BeautifulSoup(source, 'html.parser')

    countries = countries_list(soup)
    add_countries(countries)


def insert_players_from_country(continent: str, country: str) -> None:
    s = 'https://liquipedia.net/pubg/Portal:Players/' + continent
    source = requests.get(s).text
    soup = BeautifulSoup(source, 'html.parser')

    players = players_list(soup, country)
    add_players(players)


def insert_players_from_country_args() -> None:
    print(sys.argv)
    parser = argparse.ArgumentParser(
        description='Gets a string representing a continent and another string representing a country')
    parser.add_argument('-con', '--continent', type=str, required=True,
                        help="The continent from which you want to get players.")
    parser.add_argument('-cou', '--country', type=str, required=True,
                        help="The country from which you want to get players.")
    args = parser.parse_args()
    insert_players_from_country(args.continent, args.country)


def delete_continents() -> None:
    remove_all_continents()


def delete_countries() -> None:
    remove_all_countries()


def delete_players() -> None:
    remove_all_players()


def print_continents() -> None:
    print(get_all_continents())


def print_countries() -> None:
    print(get_all_countries())


def print_players() -> None:
    print(get_all_players())


def close_db() -> None:
    close_session()
