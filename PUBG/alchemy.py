from typing import List

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///games.db')

Base = declarative_base()


class Player(Base):
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
        return "{0}(Id={1}, Game_id={2}, Nick Name={3}, Name={4}, Team={5}, Links={6}, Country_id={7})"\
            .format(self.__class__.__name__, self.Id, self.Game_id, self.NickName, self.Name, self.Team, self.Links, self.Country_id)


class Game(Base):
    __tablename__ = 'games'
    Id = Column(Integer(), primary_key=True)
    Name = Column(String(30), nullable=False)

    def __repr__(self):
        return "{0}(Id={1}, Name={2})".format(self.__class__.__name__, self.Id, self.Name)


class Continent(Base):
    __tablename__ = 'continents'
    Id = Column(Integer(), primary_key=True)
    Name = Column(String(20), nullable=False)
    # Countries = relationship('Country', backref='continents')

    def __repr__(self):
        return "{0}(Id={1}, Name={2})".format(self.__class__.__name__, self.Id, self.Name)


class Country(Base):
    __tablename__ = 'countries'
    Id = Column(Integer(), primary_key=True)
    Name = Column(String(30), nullable=False)

    Continent_id = Column(Integer(), ForeignKey('continents.Id'), nullable=False)
    Continent = relationship('Continent', backref='countries')

    def __repr__(self):
        return "{0}(Id={1}, Name={2}, Continent_id={3})".format(self.__class__.__name__, self.Id, self.Name, self.Continent_id)


Base.metadata.create_all(bind=engine)

session = sessionmaker()
session.configure(bind=engine)
my_session = session()


def get_all_games() -> List[str]:
    return [g for g in my_session.query(Game)]


def get_all_players() -> List[str]:
    # return my_session.query(Player).all()
    return [p for p in my_session.query(Player)]


def get_all_countries() -> List[str]:
    return my_session.query(Country).all()


def get_all_continents() -> List[str]:
    return my_session.query(Continent).all()


def get_game_id(game_name: str) -> Integer:
    if game_name == "counterstrike":
        game_name = "Counter-Strike"
    else:
        game_name = "PUBG"

    games = my_session.query(Game)
    for game in games:
        if game.Name == game_name:
            return game.Id


def get_continent_id(continent_name: str) -> Integer:
    continents = my_session.query(Continent)
    for continent in continents:
        if continent.Name == continent_name:
            return continent.Id


def get_country_id(country_name: str) -> Integer:
    countries = my_session.query(Country)
    for country in countries:
        if country.Name == country_name:
            return country.Id


def add_continents(continents_list: List[str]) -> None:
    for c in continents_list:
        if my_session.query(Continent).filter_by(Name=c.Name).first():
            continue
        else:
            my_session.add(c)
    my_session.commit()


def add_continent(continent: Continent) -> None:
    if my_session.query(Continent).filter_by(Name=continent.Name):
        pass
    else:
        my_session.add(continent)
        my_session.commit()


def add_countries(countries_list: List[str]) -> None:
    for c in countries_list:
        if my_session.query(Country).filter_by(Name=c.Name).first():
            continue
        else:
            my_session.add(c)
    my_session.commit()


def add_country(country: Country) -> None:
    if my_session.query(Country).filter_by(Name=country.Name).first():
        pass
    else:
        my_session.add(country)
        my_session.commit()


def add_games(games_list: List[str]) -> None:
    for g in games_list:
        if my_session.query(Game).filter_by(Name=g.Name).first():
            pass
        else:
            my_session.add(g)
        my_session.commit()


def add_game(game: Game) -> None:
    if my_session.query(Game).filter_by(Name=game.Name).first():
        pass
    else:
        my_session.add(game)
        my_session.commit()


def add_players(players_list: List[str]) -> None:
    for p in players_list:
        if my_session.query(Player).filter_by(Name=p.Name).first():
            continue
        else:
            my_session.add(p)
    my_session.commit()


def add_player(player: Player) -> None:
    p = my_session.query(Player).filter_by(Name=player.Name).first()
    if p:
        if player.NickName != p.NickName or player.Team != p.Team:
            remove_player(p.Id)
        else:
            return
    my_session.add(player)
    my_session.commit()


def remove_all_continents() -> None:
    my_session.execute("DELETE FROM continents")
    my_session.commit()


def remove_all_countries() -> None:
    my_session.execute("DELETE FROM countries")
    my_session.commit()


def remove_all_games() -> None:
    my_session.execute("DELETE FROM games")
    my_session.commit()


def remove_all_players() -> None:
    my_session.execute("DELETE FROM players")
    my_session.commit()


def remove_player(id: int) -> None:
    my_session.query(Player).filter(Player.Id == id).delete()
    my_session.commit()


def close_session() -> None:
    my_session.close()
