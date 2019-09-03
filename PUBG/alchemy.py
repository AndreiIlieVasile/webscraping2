from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from typing import List


engine = create_engine('sqlite:///pubg.db')

Base = declarative_base()


class Player(Base):
    __tablename__ = 'players'
    Id = Column(Integer(), primary_key=True)
    NickName = Column(String(255))
    Name = Column(String(255), nullable=False)
    Team = Column(String(255))
    Links = Column(String(255))

    def __repr__(self):
        return "<{0} Id: {1} - Nick Name: {2}, Name: {3}, Team: {4}, Links: {5}>"\
            .format(self.__class__.__name__, self.Id, self.NickName, self.Name, self.Team, self.Links)


class Continent(Base):
    __tablename__ = 'continents'
    Id = Column(Integer(), primary_key=True)
    Name = Column(String(255), nullable=False)

    def __repr__(self):
        return "<{0} Id: {1} - Name: {2}>".format(self.__class__.__name__, self.Id, self.Name)


class Country(Base):
    __tablename__ = 'countries'
    Id = Column(Integer(), primary_key=True)
    Name = Column(String(255), nullable=False)

    def __repr__(self):
        return "<{0} Id: {1} - Name: {2}>".format(self.__class__.__name__, self.Id, self.Name)


Base.metadata.create_all(bind=engine)

session = sessionmaker()
session.configure(bind=engine)
my_session = session()


def get_all_players() -> List[str]:
    return my_session.query(Player).all()


def get_all_countries() -> List[str]:
    return my_session.query(Country).all()


def get_all_continents() -> List[str]:
    return my_session.query(Continent).all()


def add_continents(continents_list: List[str]) -> None:
    my_session.add_all(continents_list)
    my_session.commit()


def add_countries(countries_list: List[str]) -> None:
    my_session.add_all(countries_list)
    my_session.commit()


def add_players(players_list: List[str]) -> None:
    my_session.add_all(players_list)
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


def remove_all_players() -> None:
    my_session.execute("DELETE FROM players")
    my_session.commit()


def remove_player(id: int) -> None:
    my_session.query(Player).filter(Player.Id == id).delete()
    my_session.commit()


def close_session() -> None:
    my_session.close()


my_session.close()
