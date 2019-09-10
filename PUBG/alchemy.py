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
    NickName = Column(String(255))
    Name = Column(String(255), nullable=False)
    Team = Column(String(255))
    Links = Column(String(255))

    Country_name = Column(String(255), ForeignKey('countries.Name'), nullable=False)
    Country = relationship('Country', backref='players')
    Game_name = Column(String(255), ForeignKey('games.Name'), nullable=False)
    Game = relationship('Game', backref='players')

    def __repr__(self):
        return "{0}(Id={1}, Game={2}, Nick Name={3}, Name={4}, Team={5}, Links={6}, Country={7})"\
            .format(self.__class__.__name__, self.Id, self.Game_name, self.NickName, self.Name, self.Team, self.Links, self.Country_name)


class Game(Base):
    __tablename__ = 'games'
    Id = Column(Integer(), primary_key=True)
    Name = Column(String(255), nullable=False)

    def __repr__(self):
        return "{0}(Id={1}, Name={2})".format(self.__class__.__name__, self.Id, self.Name)


class Continent(Base):
    __tablename__ = 'continents'
    Id = Column(Integer(), primary_key=True)
    Name = Column(String(255), nullable=False)
    # Countries = relationship('Country', backref='continents')

    def __repr__(self):
        return "{0}(Id={1}, Name={2})".format(self.__class__.__name__, self.Id, self.Name)


class Country(Base):
    __tablename__ = 'countries'
    Id = Column(Integer(), primary_key=True)
    Name = Column(String(255), nullable=False)

    Continent_name = Column(String(255), ForeignKey('continents.Name'), nullable=False)
    Continent = relationship('Continent', backref='countries')

    def __repr__(self):
        return "{0}(Id={1}, Name={2}, Continent_name={3})".format(self.__class__.__name__, self.Id, self.Name, self.Continent_name)


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


def add_continents(continents_list: List[str]) -> None:
    for c in continents_list:
        if my_session.query(Continent).filter_by(Name=c.Name).first():
            continue
        else:
            my_session.add(c)
    my_session.commit()


def add_countries(countries_list: List[str]) -> None:
    for c in countries_list:
        if my_session.query(Country).filter_by(Name=c.Name).first():
            continue
        else:
            my_session.add(c)
    my_session.commit()


def add_games(games_list: List[str]) -> None:
    for g in games_list:
        if my_session.query(Game).filter_by(Name=g.Name).first():
            pass
        else:
            my_session.add(g)
        my_session.commit()


def add_players(players_list: List[str]) -> None:
    for p in players_list:
        if my_session.query(Player).filter_by(Name=p.Name).first():
            continue
        else:
            my_session.add(p)
    my_session.commit()


def add_player(player: Player) -> None:

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
