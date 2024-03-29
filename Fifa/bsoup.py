from typing import List
import requests
from bs4 import BeautifulSoup

from Fifa.player import Player


def names_list(soup: BeautifulSoup) -> List[str]:
    return [i.text for i in soup.find_all('a', class_='nowrap')]


def countries_list(soup: BeautifulSoup) -> List[str]:
    return [i.a.get('title') for i in soup.find_all('div', class_='bp3-text-overflow-ellipsis')
            if i.a.get('rel') == ['nofollow']]


def age_list(soup: BeautifulSoup) -> List[str]:
    return [i.text for i in soup.find_all('td', class_='col col-ae')]


def ovr_list(soup: BeautifulSoup) -> List[str]:
    return [i.span.text for i in soup.find_all('td', class_='col col-oa col-sort')]


def pot_list(soup: BeautifulSoup) -> List[str]:
    return [i.span.text for i in soup.find_all('td', class_='col col-pt')]


def team_list(soup: BeautifulSoup) -> List[str]:
    return [i.a.text for i in soup.find_all('div', class_='bp3-text-overflow-ellipsis')
            if i.a.get('rel') != ['nofollow']]


def players_per_page_list(soup: BeautifulSoup, num=60) -> List[Player]:

    names = names_list(soup)
    countries = countries_list(soup)
    ages = age_list(soup)
    ovrs = ovr_list(soup)
    pots = pot_list(soup)
    teams = team_list(soup)

    if num > len(names):  # you can have less than 60 players on a page
        num = len(names)
    players = []
    for i in range(0, num):
        p = Player(str(names[i]), str(countries[i]), int(ages[i]), int(ovrs[i]), int(pots[i]), str(teams[i]))
        players.append(p)
    return players


def get_country_id(country_name: str) -> str:
    source = requests.get('https://sofifa.com/').text
    soup = BeautifulSoup(source, 'html.parser')
    try:
        return [i.get('value') for i in soup.find_all('option', class_='cn') if i.text == str(country_name)][0]
    except IndexError:
        print('There are no players from this country; We\'ll search in the default country, England')
        return '14'
