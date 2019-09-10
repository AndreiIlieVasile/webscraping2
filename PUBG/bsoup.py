from typing import List
import requests
from bs4 import BeautifulSoup

from PUBG.alchemy import Continent, Country, Player, Game, get_game_id, get_continent_id, get_country_id


# sourcep = requests.get('https://liquipedia.net/pubg/Portal:Players/Europe').text
# sourcec = requests.get('https://liquipedia.net/counterstrike/Portal:Players/Oceania').text
# soupp = BeautifulSoup(sourcep, 'html.parser')
# soupc = BeautifulSoup(sourcec, 'html.parser')


def games_list(soup: BeautifulSoup) -> List[Game]:
    games_data = [i.a.text for i in soup.find_all("div", class_='wiki-header')]
    games = []
    for i in games_data:
        games.append(Game(Name=i))
    return games


def continents_list(game: str, soup: BeautifulSoup) -> List[Continent]:
    if game == 'counterstrike':
        ul = soup.find('ul', class_='nav nav-tabs navigation-not-searchable tabs tabs8')
        continents_data = [i.text for i in ul.find_all('li') if i.text != 'Introduction' and i.text != 'Teams']
    else:
        ul = soup.find('ul', class_='nav nav-tabs navigation-not-searchable tabs tabs6')
        continents_data = [i.text for i in ul.find_all('li') if i.text != 'Introduction']
    continents = []
    for i in continents_data:
        continents.append(Continent(Name=i))
    return continents


def countries_list(game: str, soup: BeautifulSoup, continent: str) -> List[Country]:
    continentid = get_continent_id(continent)
    if game == 'counterstrike':
        countries_data = [i.a.get('title') for i in soup.find_all('table', class_='wikitable collapsible collapsed')]
    else:
        countries_data = [i.a.get('title') for i in soup.find_all('table', class_='wikitable collapsible smwtable')]
    countries = []
    for i in countries_data:
        countries.append(Country(Name=i, Continent_id=continentid))
    return countries


def players_list_pubg(game: str, soup: BeautifulSoup, country: str) -> List[Player]:
    players = []
    gameid = get_game_id(game)
    countryid = get_country_id(country)
    i = soup.find(lambda tag: tag.name == "th" and country in tag.text).find_parents('tr')[0]
    for j in i.find_next_siblings('tr'):
        if j.findChildren('td'):
            player_data = j.text.strip("\n")
            player_data = player_data.strip(" ")
            player_data = player_data.split("\n")
            for k in j.findChildren('a', class_='external text'):
                player_data[3] = k.get('href')
            players.append(
                Player(NickName=player_data[0], Name=player_data[1], Team=player_data[2],
                       Links=player_data[3], Country_id=countryid, Game_id=gameid))
    return players


def players_list_cs(game: str, soup: BeautifulSoup, country: str) -> List[Player]:
    players = []
    gameid = get_game_id(game)
    countryid = get_country_id(country)
    i = soup.find(lambda tag: tag.name == "th" and country in tag.text).find_parents('tr')[0]
    for j in i.find_next_siblings('tr'):
        player_data = j.text.strip()
        player_data = player_data.split(" - ")
        player_data.extend([None])
        if j.findChildren("div"):
            player_data[2] = j.div.span.a.get('title')
        players.append(Player(NickName=player_data[0], Name=player_data[1], Team=player_data[2],
                              Country_id=countryid, Game_id=gameid))
    return players


# print(players_list_pubg("pubg", soupp, 'France'))
# print(players_list_cs("counterstrike", soupc, "New Zealand"))
