from dataclasses import dataclass


@dataclass
class Player:

    def __init__(self, name: str, country: str, age: int, ovr: int, pot: int, team: str) -> None:
        self._name = name
        self._country = country
        self._age = age
        self._ovr = ovr
        self._pot = pot
        self._team = team

    def get_name(self) -> str:
        return self._name

    def get_country(self) -> str:
        return self._country

    def get_age(self) -> int:
        return self._age

    def get_ovr(self) -> int:
        return self._ovr

    def get_pot(self) -> int:
        return self._pot

    def get_team(self) -> str:
        return self._team

    def __str__(self) -> str:
        return "Player name: " + self._name + " country: " + self._country + " age: " + str(self._age) + " OVR: " + \
               str(self._ovr) + " POT: " + str(self._pot) + " team: " + self._team
