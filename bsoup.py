from bs4 import BeautifulSoup
import requests
from Player import Player


def names_list(soup):
    return [i.text for i in soup.find_all('a', class_='nowrap')]


def countries_list(soup):
    return [i.a.get('title') for i in soup.find_all('div', class_='bp3-text-overflow-ellipsis') if i.a.get('rel') == ['nofollow']]


def ovr_list(soup):
    return [i.span.text for i in soup.find_all('td', class_='col col-oa')]


def pot_list(soup):
    return [i.span.text for i in soup.find_all('td', class_='col col-pt')]


def players_per_page_list(soup, num=60):
    names = names_list(soup)
    countries = countries_list(soup)
    ovrs = ovr_list(soup)
    pots = pot_list(soup)

    if num > len(names):                #you can have less than 60 players on a page
        num = len(names)
    players = []
    for i in range(0, num):
        p = Player(names[i], countries[i], ovrs[i], pots[i])
        players.append(p.__str__())
    return players


def get_country_id(c):
    source = requests.get('https://sofifa.com/').text
    soup = BeautifulSoup(source, 'html.parser')
    try:
        return [i.get('value') for i in soup.find_all('option', class_='cn') if i.text == str(c)][0]
    except IndexError:
        print('There are no players from this country; We\'ll search in the default country, England')
        return '14'
