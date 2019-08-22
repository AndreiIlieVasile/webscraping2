from dataclasses import dataclass


@dataclass
class Player:

    def __init__(self, name, country, age, ovr, pot, team):
        self._name = name
        self._country = country
        self._age = age
        self._ovr = ovr
        self._pot = pot
        self._team = team

    def get_name(self):
        return self._name

    def get_country(self):
        return self._country

    def get_age(self):
        return self._age

    def get_ovr(self):
        return self._ovr

    def get_pot(self):
        return self._pot

    def get_team(self):
        return self._team

    def __str__(self):
        return "Player name: " + self._name + " country: " + self._country + " age: " + str(self._age) + " OVR: " + str(self._ovr) + " POT: " + str(self._pot) + " team: " + self._team
