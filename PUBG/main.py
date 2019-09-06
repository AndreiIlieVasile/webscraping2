import argparse
import sys

import requests
from bs4 import BeautifulSoup

from PUBG.alchemy import *
from PUBG.bsoup import continents_list, countries_list, players_list, games_list

LINK = 'https://liquipedia.net//Portal:Players'


def insert_games() -> None:
    link = LINK[:22]
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'html.parser')

    games = games_list(soup)
    add_games(games)


def insert_continents(game: str) -> None:
    link = LINK[:23] + game + LINK[23:]
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'html.parser')

    continents = continents_list(game, soup)
    add_continents(continents)


def insert_countries_from_continent(game: str, continent: str) -> None:
    link = LINK[:23] + game + LINK[23:] + '/' + continent
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'html.parser')

    countries = countries_list(game, soup, continent)
    add_countries(countries)


def insert_players_from_country(game: str, continent: str, country: str) -> None:
    link = LINK[:23] + game + LINK[23:] + '/' + continent
    source = requests.get(link).text
    soup = BeautifulSoup(source, 'html.parser')

    players = players_list(game, soup, country)
    add_players(players)


def insert_players_from_country_args() -> None:
    print(sys.argv)
    parser = argparse.ArgumentParser(
        description='Gets a string representing a game, one representing a continent'
                    ' and another string representing a country')
    parser.add_argument('-g', '--game', type=str, required=True,
                        help="The continent from which you want to get players.")
    parser.add_argument('-con', '--continent', type=str, required=True,
                        help="The continent from which you want to get players.")
    parser.add_argument('-cou', '--country', type=str, required=True,
                        help="The country from which you want to get players.")
    args = parser.parse_args()
    insert_players_from_country(args.game, args.continent, args.country)


def delete_continents() -> None:
    remove_all_continents()


def delete_countries() -> None:
    remove_all_countries()


def delete_game() -> None:
    remove_all_games()


def delete_players() -> None:
    remove_all_players()


def print_continents() -> None:
    print(get_all_continents())


def print_countries() -> None:
    print(get_all_countries())


def print_games() -> None:
    print(get_all_games())


def print_players() -> None:
    print(get_all_players())


def close_db() -> None:
    close_session()
