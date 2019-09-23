import re
from typing import List

from bs4 import BeautifulSoup

from PUBG.alchemy import Continent, Country, Player, Game, get_game_id, get_continent_id, get_country_id


# import requests
# sourcep = requests.get('https://liquipedia.net/pubg/Portal:Players/Europe').text
# sourcec = requests.get('https://liquipedia.net/counterstrike/Portal:Players/Oceania').text


def games_list(source: str) -> List[Game]:
    """
    Creates a list of games
    :param source: The link to the webpage
    :return: A list of games
    """
    soup = BeautifulSoup(source, 'html.parser')
    games_data = [i.a.text for i in soup.find_all("div", class_='wiki-header')]
    games = []
    for i in games_data:
        games.append(Game(Name=i))
    return games


def continents_list(game_name: str, source: str) -> List[Continent]:
    """
    Creates a list of continents
    :param game_name: The game's name
    :param source: The link to the webpage
    :return: A list of continents
    """
    soup = BeautifulSoup(source, 'html.parser')
    if game_name == 'counterstrike':
        ul_tag = soup.find('ul', class_='nav nav-tabs navigation-not-searchable tabs tabs8')
        continents_data = [i.text for i in ul_tag.find_all('li') if i.text != 'Introduction' and i.text != 'Teams']
    else:
        ul_tag = soup.find('ul', class_='nav nav-tabs navigation-not-searchable tabs tabs6')
        continents_data = [i.text for i in ul_tag.find_all('li') if i.text != 'Introduction']
    continents = []
    for i in continents_data:
        continents.append(Continent(Name=i))
    return continents


def countries_list(game_name: str, source: str, continent_name: str) -> List[Country]:
    """
    Creates a list of countries
    :param game_name: The game's name
    :param source: The link to the webpage
    :param continent_name: The continent's name
    :return: A list of countries
    """
    soup = BeautifulSoup(source, 'html.parser')
    continent_id = get_continent_id(continent_name=continent_name)
    if game_name == 'counterstrike':
        countries_data = [i.a.get('title') for i in soup.find_all('table', class_='wikitable collapsible collapsed')]
    else:
        countries_data = [i.a.get('title') for i in soup.find_all('table', class_='wikitable collapsible smwtable')]
    countries = []
    for i in countries_data:
        countries.append(Country(Name=i, Continent_id=continent_id))
    return countries


def players_data_pubg(player_info: str, player_link: str) -> dict:
    """
    Creates a dictionary with a pubg player's data
    :param player_info: A string that contains the nickname, name and team of the player
    :param player_link: A string that contains the link to a player's webpage
    :return: The dictionary
    """
    player_dict = {}
    pattern = re.compile(r'[^\s].*[^\s]')
    matches = pattern.findall(player_info)
    player_dict['NickName'] = matches[0]
    player_dict['Name'] = matches[1]
    if len(matches) == 3:
        player_dict['Team'] = matches[2]

    pattern_link = re.compile(r'^http.*')
    match = pattern_link.findall(player_link)
    if match:
        player_dict['Link'] = match[0]
    return player_dict


def players_list_pubg(game_name: str, source: str, country_name: str) -> List[Player]:
    """
    Creates a list of pubg players
    :param game_name: The game's name
    :param source:  The link to the webpage
    :param country_name: The country's name
    :return: The list of players
    """
    soup = BeautifulSoup(source, 'html.parser')
    players = []
    game_id = get_game_id(game_name=game_name)
    country_id = get_country_id(country_name=country_name)
    i = soup.find(lambda tag: tag.name == "th" and country_name in tag.text).find_parents('tr')[0]
    for j in i.find_next_siblings('tr'):
        if j.findChildren('td'):
            player_info = j.text
            player_link = ""
            for k in j.findChildren('a', class_='external text'):
                player_link = k.get('href')
            player_dict = players_data_pubg(player_info=player_info, player_link=player_link)
            players.append(
                Player(NickName=player_dict.get('NickName', None),
                       Name=player_dict.get('Name', None),
                       Team=player_dict.get('Team', None),
                       Links=player_dict.get('Link', None),
                       Country_id=country_id,
                       Game_id=game_id))
    return players


def players_data_cs(player_info: str, player_team: str) -> dict:
    """
    Creates a dictionary with a counterstrike player's data
    :param player_info: A string which contains the nickname and name of the player
    :param player_team: A string which contains the player's team
    :return: The dictionary
    """
    player_dict = {}
    # pattern = re.compile(r'[a-zA-Z]*[a-zA-Z\sa-zA-Z]*')
    pattern = re.compile(r'\s*(.*)(\s-\s)([A-Z]\w*\s[A-Z]\w*)\s*')
    matches = pattern.finditer(player_info)
    for match in matches:
        player_dict['NickName'] = match.group(1)
        player_dict['Name'] = match.group(3)

    pattern_team = re.compile(r'(.*[\s]?.*)')
    match = pattern_team.findall(player_team)
    if match:
        player_dict['Team'] = match[0]
    return player_dict


def players_list_cs(game_name: str, source: str, country_name: str) -> List[Player]:
    """
    Creates a list of counterstrike players
    :param game_name: The game's name
    :param source: The link to the webpage
    :param country_name: The country's name
    :return: The list of players
    """
    soup = BeautifulSoup(source, 'html.parser')
    players = []
    game_id = get_game_id(game_name=game_name)
    country_id = get_country_id(country_name=country_name)
    i = soup.find(lambda tag: tag.name == "th" and country_name in tag.text).find_parents('tr')[0]
    for j in i.find_next_siblings('tr'):
        player_info = j.text
        player_team = ""
        if j.findChildren("div"):
            player_team = j.div.span.a.get('title')
        player_dict = players_data_cs(player_info=player_info, player_team=player_team)
        players.append(
            Player(NickName=player_dict.get('NickName', None),
                   Name=player_dict.get('Name', None),
                   Team=player_dict.get('Team', None),
                   Country_id=country_id,
                   Game_id=game_id))
    return players

# print(players_list_pubg("pubg", sourcep, 'Germany'))
# print(players_list_cs("counterstrike", sourcec, "New Zealand"))
