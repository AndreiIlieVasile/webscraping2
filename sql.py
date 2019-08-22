import sqlite3
from Player import Player


class DB:
    def __init__(self, dbname):
        self._dbname = dbname
        #self._connection = sqlite3.connect(str(self._dbname))
        self._connection = sqlite3.connect(':memory:')
        self._cursor = self._connection.cursor()

    def close_connection(self):
        self._connection.close()

    def create_players_table(self):
        self._cursor.execute("""CREATE TABLE players (
                                                name text,
                                                country text,
                                                ovr integer,
                                                pot integer
                                                )""")

    def insert(self, player):
        with self._connection:
            #self._cursor.execute("INSERT INTO players VALUES (?, ?, ?, ?)", (player.getName(), player.getCountry(), player.getOvr(), player.getPot()))
            self._cursor.execute("INSERT INTO players VALUES (:name, :country, :ovr, :pot)", {'name': player.getName(), 'country': player.getCountry(), 'ovr': player.getOvr(), 'pot': player.getPot()})

    def get_players_by_ovr(self):
        self._cursor.execute('SELECT * FROM players ORDER BY ovr DESC')
        return self._cursor.fetchall()

    def clear_db(self):
        with self._connection:
            self._cursor.execute("DELETE FROM players")

    def remove(self, player):
        with self._connection:
            self._cursor.execute("DELETE FROM players WHERE name = :name", {'name': player.getName()})
