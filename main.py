import argparse
import sys

import requests
from bs4 import BeautifulSoup

from bsoup import players_per_page_list, get_country_id
from sql import DB


class Run:
    def __init__(self):
        self._database = DB('players.db')
        # self._database = DB()

    def get_players_from_country(self, country, num):
        self._database.create_players_table()
        # self._database.clear_db()

        cid = get_country_id(country)
        num_players_left = num % 60
        num_pages = num // 60 + 1
        page = 0
        while page < num_pages:
            s = 'https://sofifa.com/players?type=all&na%5B%5D=' + cid + '&offset=' + str(page * 60)
            source = requests.get(s).text
            soup = BeautifulSoup(source, 'html.parser')
            if page == num_pages-1:
                players = players_per_page_list(soup, num_players_left)
            else:
                players = players_per_page_list(soup)
            for i in players:
                self._database.insert(i)
            page += 1
        return self._database.get_players_by_ovr()

    def filter_young_pot(self):
        return self._database.get_players_by_age_and_pot()

    def close_db(self):
        self._database.close_connection()

    def main(self):
        print(sys.argv)
        parser = argparse.ArgumentParser(description='Gets a string representing a country and an integer representing the number of results')
        parser.add_argument('-c', '--country', type=str, required=True, help="The country from which you want to sort.")
        parser.add_argument('-n', '--number', type=int, required=True, help="The number of players you want in the result.")
        args = parser.parse_args()
        self.get_players_from_country(args.country, args.number)
        print(*self.filter_young_pot(), sep='\n')
