from typing import List, Union

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///games.db')

Base = declarative_base()


class Game(Base):
    """
    Class for game objects
    """
    __tablename__ = 'games'
    Id = Column(Integer(), primary_key=True)
    Name = Column(String(30), nullable=False)

    def __repr__(self):
        return "{0}(Id={1}, Name={2})".format(self.__class__.__name__, self.Id, self.Name)


class Continent(Base):
    """
    Class for continent objects
    """
    __tablename__ = 'continents'
    Id = Column(Integer(), primary_key=True)
    Name = Column(String(20), nullable=False)

    def __repr__(self):
        return "{0}(Id={1}, Name={2})".format(self.__class__.__name__, self.Id, self.Name)


class Country(Base):
    """
    Class for country objects
    """
    __tablename__ = 'countries'
    Id = Column(Integer(), primary_key=True)
    Name = Column(String(30), nullable=False)
    Continent_id = Column(Integer(), ForeignKey('continents.Id'), nullable=False)

    Continent = relationship('Continent', backref='countries')

    def __repr__(self):
        return "{0}(Id={1}, Name={2}, Continent_id={3})".format(self.__class__.__name__, self.Id,
                                                                self.Name, self.Continent_id)


class Player(Base):
    """
    Class for player objects
    """
    __tablename__ = 'players'
    Id = Column(Integer(), primary_key=True)
    NickName = Column(String(30), nullable=False)
    Name = Column(String(30), nullable=False)
    Team = Column(String(40))
    Links = Column(String(100))
    Country_id = Column(Integer(), ForeignKey('countries.Id'), nullable=False)
    Game_id = Column(Integer(), ForeignKey('games.Id'), nullable=False)

    Country = relationship('Country', backref='players')
    Game = relationship('Game', backref='players')

    def __repr__(self):
        return "{0}(Id={1}, Game_id={2}, Nick Name={3}, Name={4}, Team={5}, Links={6}, Country_id={7})" \
            .format(self.__class__.__name__, self.Id, self.Game_id, self.NickName,
                    self.Name, self.Team, self.Links, self.Country_id)

    def update(self, player):
        """
        Updates a player's nickname, team and link
        :param player: The player
        :return: -
        """
        self.NickName = player.NickName
        self.Team = player.Team
        self.Links = player.Links


Base.metadata.create_all(bind=engine)

session = sessionmaker()
session.configure(bind=engine)
my_session = session()


def get_all_games() -> List[Game]:
    """
    :return: The list of games from th db
    """
    return my_session.query(Game).all()


def get_all_continents() -> List[Continent]:
    """
    :return: The list of continents from th db
    """
    return my_session.query(Continent).all()


def get_all_countries() -> List[Country]:
    """
    :return: The list of countries from th db
    """
    return my_session.query(Country).all()


def get_all_players() -> List[Player]:
    """
    :return: The list of players from th db
    """
    return my_session.query(Player).all()


def get_game_id(game_name: str) -> Union[int, None]:
    """
    :param game_name: The game's name
    :return: The id of the game
    """
    game_names_dict = {'counterstrike': 'Counter-Strike', 'pubg': 'PUBG'}
    game = my_session.query(Game).filter_by(Name=game_names_dict[game_name]).first()
    if game:
        return game.Id


def get_continent_id(continent_name: str) -> Union[int, None]:
    """
    :param continent_name: The continent's name
    :return: The id of the continent
    """
    continent = my_session.query(Continent).filter_by(Name=continent_name).first()
    if continent:
        return continent.Id


def get_country_id(country_name: str) -> Union[int, None]:
    """
    :param country_name: The country's name
    :return: The id of the country
    """
    country = my_session.query(Country).filter_by(Name=country_name).first()
    if country:
        return country.Id


def add_games(games_list: List[Game]) -> None:
    """
    Inserts a list of games in db
    :param games_list: The list of games
    :return: -
    """
    for game in games_list:
        if my_session.query(Game).filter_by(Name=game.Name).first():
            pass
        my_session.add(game)
    my_session.commit()


def add_continents(continents_list: List[Continent]) -> None:
    """
    Inserts a list of continents in db
    :param continents_list: The list of continents
    :return: -
    """
    for continent in continents_list:
        if my_session.query(Continent).filter_by(Name=continent.Name).first():
            continue
        my_session.add(continent)
    my_session.commit()


def add_countries(countries_list: List[Country]) -> None:
    """
    Inserts a list of countries in db
    :param countries_list: The list of countries
    :return: -
    """
    for country in countries_list:
        if my_session.query(Country).filter_by(Name=country.Name).first():
            continue
        my_session.add(country)
    my_session.commit()


def add_players(players_list: List[Player]) -> None:
    """
    Inserts a list of players in db
    :param players_list: The list of players
    :return: -
    """
    for player in players_list:
        player_db = my_session.query(Player).filter_by(Name=player.Name).first()
        if player_db:
            player_db.update(player)
        else:
            my_session.add(player)
    my_session.commit()


def add_game(game: Game) -> None:
    """
    Inserts a game in db
    :param game: the game
    :return: -
    """
    if my_session.query(Game).filter_by(Name=game.Name).first():
        return
    my_session.add(game)
    my_session.commit()


def add_continent(continent: Continent) -> None:
    """
    Inserts a continent in db
    :param continent: the continent
    :return: -
    """
    if my_session.query(Continent).filter_by(Name=continent.Name).first():
        return
    my_session.add(continent)
    my_session.commit()


def add_country(country: Country) -> None:
    """
    Inserts a country in db
    :param country: the country
    :return: -
    """
    if my_session.query(Country).filter_by(Name=country.Name).first():
        return
    my_session.add(country)
    my_session.commit()


def add_player(player: Player) -> None:
    """
    Inserts a player in db
    :param player: the player
    :return: -
    """
    player_db = my_session.query(Player).filter_by(Name=player.Name).first()
    if player_db:
        player_db.update(player)
    else:
        my_session.add(player)
    my_session.commit()


def remove_all_games() -> None:
    """
    Removes all the games from db
    :return: -
    """
    my_session.query(Game).delete()
    my_session.commit()


def remove_all_continents() -> None:
    """
    Removes all the continents from db
    :return: -
    """
    my_session.query(Continent).delete()
    my_session.commit()


def remove_all_countries() -> None:
    """
    Removes all the countries from db
    :return: -
    """
    my_session.query(Country).delete()
    my_session.commit()


def remove_all_players() -> None:
    """
    Removes all the players from db
    :return: -
    """
    my_session.query(Player).delete()
    my_session.commit()


def remove_player(player_id: int) -> None:
    """
    Removes a player from db
    :param player_id: The player's id
    :return: -
    """
    my_session.query(Player).filter(Player.Id == player_id).delete()
    my_session.commit()


def close_session() -> None:
    """
    Closes the session
    :return: -
    """
    my_session.close()
