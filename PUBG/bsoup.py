from typing import List
import requests
from bs4 import BeautifulSoup

from PUBG.alchemy import Continent, Country, Player


# source = requests.get('https://liquipedia.net/pubg/Portal:Players/Europe').text
# soup = BeautifulSoup(source, 'html.parser')


def continents_data(soup: BeautifulSoup) -> List[str]:
    ul = soup.find('ul', class_='nav nav-tabs navigation-not-searchable tabs tabs6')
    return [i.text for i in ul.find_all('li')
            if i.text != 'Introduction']


def countries_data(soup: BeautifulSoup) -> List[str]:
    return [i.a.get('title') for i in soup.find_all('table', class_='wikitable collapsible smwtable')]


def players_data(soup: BeautifulSoup, country: str) -> List[str]:
    table = [i for i in soup.find_all(class_='wikitable collapsible smwtable')
             if i.a.get('title') == country]
    list_table = []
    for i in table:
        list_table.append(i.get_text())
    s = [x.split('\n') for x in list_table]
    s = s[0]

    s = str(s)
    s = s.replace("'", "")
    s = s.strip(',')
    s = s.replace(",", "")

    s = s.strip(']')
    s = s.strip('[')
    s = s.split("   ")
    return s[3:]


def continents_list(soup: BeautifulSoup) -> List[Continent]:
    data = continents_data(soup)
    continents = []
    for i in range(0, len(data)):
        continents.append(Continent(Name=str(data[i])))
    return continents


def countries_list(soup: BeautifulSoup) -> List[Country]:
    data = countries_data(soup)
    countries = []
    for i in range(0, len(data)):
        countries.append(Country(Name=str(data[i])))
    return countries


def players_list(soup: BeautifulSoup, country: str) -> List[Player]:
    data = players_data(soup, country)
    players = []

    for i in range(0, len(data)-4, 4):
        players.append(Player(NickName=str(data[i]), Name=str(data[i+1]), Team=str(data[i+2]), Links=str(data[i+3])))
    return players




# def players_data_tag(soup: BeautifulSoup, country: str) -> List[str]:
#     c = soup.find(class_='wikitable collapsible smwtable')
#     return [i.text for i in c.find_all('td')]


# print(continents_data(soup))
# print(type(countries_data(soup)))
# print(players_data(soup, 'Germany'))

# print(players_data_tag(soup, 'Romania'))
