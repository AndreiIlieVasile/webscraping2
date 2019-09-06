from typing import List
import requests
from bs4 import BeautifulSoup

from PUBG.alchemy import Continent, Country, Player, Game


# sourcep = requests.get('https://liquipedia.net/pubg/Portal:Players/Europe').text
# sourcec = requests.get('https://liquipedia.net/counterstrike/Portal:Players/Europe').text
# soupp = BeautifulSoup(sourcep, 'html.parser')
# soupc = BeautifulSoup(sourcec, 'html.parser')

def games_data(soup: BeautifulSoup) -> List[str]:
    return [i.a.text for i in soup.find_all("div", class_='wiki-header')]


def continents_data_pubg(soup: BeautifulSoup) -> List[str]:
    ul = soup.find('ul', class_='nav nav-tabs navigation-not-searchable tabs tabs6')
    return [i.text for i in ul.find_all('li')
            if i.text != 'Introduction']


def continents_data_cs(soup: BeautifulSoup) -> List[str]:
    ul = soup.find('ul', class_='nav nav-tabs navigation-not-searchable tabs tabs8')
    return [i.text for i in ul.find_all('li')
            if i.text != 'Introduction' and i.text != 'Teams']


def countries_data_pubg(soup: BeautifulSoup) -> List[str]:
    return [i.a.get('title') for i in soup.find_all('table', class_='wikitable collapsible smwtable')]


def countries_data_cs(soup: BeautifulSoup) -> List[str]:
    return [i.a.get('title') for i in soup.find_all('table', class_='wikitable collapsible collapsed')]


def players_data_pubg(soup: BeautifulSoup, country: str) -> List[List]:
    players = []
    for i in soup.find_all('table', class_='wikitable collapsible smwtable'):
        header = i.find('th')
        if header.text == "  " + country:
            for j in i.find_all('tr'):
                if j.findChildren('td'):
                    pd = j.text.strip("\n")
                    pd = pd.strip(" ")
                    pd = pd.split("\n")
                    for k in j.findChildren('a', class_='external text'):
                        pd[3] = k.get('href')
                    players.append(pd)
    return players


def players_data_cs(soup: BeautifulSoup, country: str) -> List[List]:
    players = []
    for i in soup.find_all('div', class_='template-box'):
        if i.tr.text == " " + country:
            for j in i.find_all('td'):
                pd = j.text.lstrip(" ")
                pd = pd.rstrip(" ")
                pd = pd.split(" - ")
                if j.findChildren("div", recursive=False):
                    players.append([pd[0], pd[1], j.div.span.a.get('title')])
                else:
                    players.append([pd[0], pd[1]])
    return players


def continents_list(game: str, soup: BeautifulSoup) -> List[Continent]:
    if game == 'counterstrike':
        data = continents_data_cs(soup)
    else:
        data = continents_data_pubg(soup)
    continents = []
    for i in range(0, len(data)):
        continents.append(Continent(Name=str(data[i])))
    return continents


def countries_list(game: str, soup: BeautifulSoup, continent: str) -> List[Country]:
    if game == 'counterstrike':
        data = countries_data_cs(soup)
    else:
        data = countries_data_pubg(soup)
    countries = []
    for i in range(0, len(data)):
        countries.append(Country(Name=str(data[i]), Continent_name=continent))
    return countries


def games_list(soup: BeautifulSoup) -> List[Game]:
    data = games_data(soup)
    games = []
    for i in range(0, len(data)):
        games.append(Game(Name=str(data[i])))
    return games


def players_list(game: str, soup: BeautifulSoup, country: str) -> List[Player]:
    players = []
    if game == 'counterstrike':
        data = players_data_cs(soup, country)
        for i in data:
            if len(i) < 3:
                players.append(Player(NickName=i[0], Name=i[1], Country_name=country, Game_name=game))
            else:
                players.append(Player(NickName=i[0], Name=i[1], Team=i[2], Country_name=country, Game_name=game))
    else:
        data = players_data_pubg(soup, country)
        for i in data:
            if i[2] == ' ':
                players.append(Player(NickName=i[0], Name=i[1], Links=i[3], Country_name=country, Game_name=game))
            else:
                players.append(Player(NickName=i[0], Name=i[1], Team=i[2], Links=i[3], Country_name=country, Game_name=game))
    return players


# print(players_list('cs', soupc, 'Germany'))
# print(players_list('pubg', soupp, 'Germany'))
