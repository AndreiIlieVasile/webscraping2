from bsoup import players_per_page_list, get_country_id
from sql import DB
import argparse
from bs4 import BeautifulSoup
import requests
import sys


def filter_by_country(country, num):
    db = DB('players.db')
    db.create_players_table()
    db.clear_db()

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
            db.insert(i)
        page += 1
    result = db.get_players_by_ovr()
    db.close_connection()
    return result


def main():
    print(sys.argv)
    parser = argparse.ArgumentParser(description='Gets a string representing a country and an integer representing the number of results')
    parser.add_argument('-c', '--country', type=str, required=True, help="The country from which you want to sort.")
    parser.add_argument('-n', '--number', type=int, required=True, help="The number of players you want in the result.")
    args = parser.parse_args()
    print(filter_by_country(args.country, args.number))


if __name__ == '__main__':
    main()
