from dataclasses import dataclass


@dataclass
class Player:

    def __init__(self, name, country, ovr, pot):
        self._name = name
        self._country = country
        self._ovr = ovr
        self._pot = pot

    def getName(self):
        return self._name

    def getCountry(self):
        return self._country

    def getOvr(self):
        return self._ovr

    def getPot(self):
        return self._pot

    def __str__(self):
        return "Player name: " + self._name + " country: " + self._country + " OVR: " + str(self._ovr) + " POT: " + str(self._pot)
