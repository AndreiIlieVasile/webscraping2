import sqlite3
from typing import List

from Fifa.player import Player


class DB:
    def __init__(self, dbname=":memory:"):
        self._dbname = dbname
        self._connection = sqlite3.connect(str(self._dbname))
        self._cursor = self._connection.cursor()

    def close_connection(self) -> None:
        self._connection.close()

    def create_players_table(self) -> None:
        self._cursor.execute("""CREATE TABLE IF NOT EXISTS players (
                                                name text,
                                                country text,
                                                age integer,
                                                ovr integer,
                                                pot integer,
                                                team text
                                                )""")

    def insert(self, player: Player) -> None:
        with self._connection:
            # self._cursor.execute("INSERT INTO players VALUES (?, ?, ?, ?, ?, ?)", (player.get_name(),
            # player.get_country(), player.get_age(), player.get_ovr(), player.get_pot(), player.get_pot()))
            self._cursor.execute("INSERT INTO players VALUES (:name, :country, :age, :ovr, :pot, :team)",
                                 {'name': player.get_name(), 'country': player.get_country(), 'age': player.get_age(),
                                  'ovr': player.get_ovr(), 'pot': player.get_pot(), 'team': player.get_team()})

    def get_players_by_ovr(self) -> List[str]:
        self._cursor.execute('SELECT * FROM players ORDER BY ovr DESC')
        return self._cursor.fetchall()

    def get_players_by_age_and_pot(self) -> List[str]:
        self._cursor.execute('SELECT * FROM (SELECT * FROM players ORDER BY age LIMIT 10) ORDER BY pot DESC')
        return self._cursor.fetchall()

    def clear_db(self) -> None:
        with self._connection:
            self._cursor.execute("DELETE FROM players")

    def remove(self, player: Player) -> None:
        with self._connection:
            self._cursor.execute("DELETE FROM players WHERE name = :name", {'name': player.get_name()})
