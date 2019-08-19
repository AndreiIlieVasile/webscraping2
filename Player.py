from dataclasses import dataclass


@dataclass
class Player:

    def __init__(self, name, country, ovr, pot):
        self._name = name
        self._country = country
        self._ovr = ovr
        self._pot = pot

    def __str__(self):
        return "Player name: " + self._name + " country: " + self._country + " OVR: " + self._ovr + " POT: " + self._pot
