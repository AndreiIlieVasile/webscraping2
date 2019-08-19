from bs4 import BeautifulSoup
import requests
from Player import Player


source = requests.get('https://sofifa.com/?hl=en-US').text

soup = BeautifulSoup(source, 'html.parser')


def names_list():
    return [i.text for i in soup.find_all('a', class_='nowrap')]


def countries_list():
    return [i.a.get('title') for i in soup.find_all('div', class_='bp3-text-overflow-ellipsis') if i.a.get('rel') == ['nofollow']]


def ovr_list():
    return [i.span.text for i in soup.find_all('td', class_='col col-oa')]


def pot_list():
    return [i.span.text for i in soup.find_all('td', class_='col col-pt')]


names = names_list()
countries = countries_list()
ovrs = ovr_list()
pots = pot_list()

players = []
for i in range(0, len(names)):
    p = Player(names[i], countries[i], ovrs[i], pots[i])
    players.append(p.__str__())

print("\n".join(players))
