import argparse
import sys

import requests

from PUBG.alchemy import (get_all_games, get_all_continents, get_all_countries, get_all_players,
                          add_games, add_continents, add_countries, add_players, remove_all_games,
                          remove_all_continents, remove_all_countries, remove_all_players, close_session)
from PUBG.bsoup import continents_list, countries_list, players_list_pubg, players_list_cs, games_list


LINK = 'https://liquipedia.net//Portal:Players'


def insert_games() -> None:
    """
    Inserts a list of games in the db
    :return: -
    """
    link = LINK[:22]
    source = requests.get(link).text

    games = games_list(source=source)
    add_games(games_list=games)


def insert_continents(game_name: str) -> None:
    """
    Inserts a list of continents in the db
    :param game_name: The game's name
    :return: -
    """
    link = LINK[:23] + game_name + LINK[23:]
    source = requests.get(link).text

    continents = continents_list(game_name=game_name, source=source)
    add_continents(continents_list=continents)


def insert_countries_from_continent(game_name: str, continent_name: str) -> None:
    """
    Inserts a list of countries in the db
    :param game_name: The game's name
    :param continent_name: The continent's name
    :return: -
    """
    link = LINK[:23] + game_name + LINK[23:] + '/' + continent_name
    source = requests.get(link).text

    countries = countries_list(game_name=game_name, source=source, continent_name=continent_name)
    add_countries(countries_list=countries)


def insert_players_from_country(game_name: str, continent: str, country_name: str) -> None:
    """
    Inserts a list of players in the db
    :param game_name: The game's name
    :param continent: The continent's name
    :param country_name: The country's name
    :return: -
    """
    if game_name not in ['counterstrike', 'pubg']:
        return
    link = LINK[:23] + game_name + LINK[23:] + '/' + continent
    source = requests.get(link).text
    # fail early and constants
    if game_name == 'counterstrike':
        players = players_list_cs(game_name=game_name, source=source, country_name=country_name)
    elif game_name == 'pubg':
        players = players_list_pubg(game_name=game_name, source=source, country_name=country_name)
    add_players(players_list=players)


def insert_players_from_country_args() -> None:
    """
    Inserts a list of players in the db
    :return: -
    """
    print(sys.argv)
    parser = argparse.ArgumentParser(
        description='Gets a string representing a game, one representing a continent'
                    ' and another string representing a country')
    parser.add_argument('-g', '--game', type=str, required=True,
                        help="The game from which you want to get players.")
    parser.add_argument('-con', '--continent', type=str, required=True,
                        help="The continent from which you want to get players.")
    parser.add_argument('-cou', '--country', type=str, required=True,
                        help="The country from which you want to get players.")
    args = parser.parse_args()
    insert_players_from_country(args.game, args.continent, args.country)


def delete_games() -> None:
    """
    Removes all games from the db
    :return:
    """
    remove_all_games()


def delete_continents() -> None:
    """
    Removes all continents from the db
    :return: -
    """
    remove_all_continents()


def delete_countries() -> None:
    """
    Removes all countries from the db
    :return: -
    """
    remove_all_countries()


def delete_players() -> None:
    """
    Removes all players from the db
    :return: -
    """
    remove_all_players()


def print_games() -> None:
    """
    Prints all games from the db
    :return: -
    """
    print(get_all_games())


def print_continents() -> None:
    """
    Prints all continents from the db
    :return: -
    """
    print(get_all_continents())


def print_countries() -> None:
    """
    Prints all countries from the db
    :return: -
    """
    print(get_all_countries())


def print_players() -> None:
    """
    Prints all players from the db
    :return: -
    """
    print(get_all_players())


def close_db() -> None:
    """
    Closes the db
    :return: -
    """
    close_session()
