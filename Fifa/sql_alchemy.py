from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, MetaData, Column, Integer, String
from typing import List


# engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///alchemyplayers.db')

Base = declarative_base()


class Player(Base):
    __tablename__ = "players"

    Id = Column(Integer(), primary_key=True, unique=True)
    Name = Column(String(255), nullable=False)
    Country = Column(String(255))
    Age = Column(Integer())
    Ovr = Column(Integer())
    Pot = Column(Integer())
    Team = Column(String(255), default='Free agent')

    def __repr__(self):
        return "<{0} Id: {1} - Name: {2}, Country: {3}, Age: {4}, Ovr: {5}, Pot: {6}, Team: {7}>"\
            .format(self.__class__.__name__, self.Id, self.Name, self.Country, self.Age, self.Ovr, self.Pot, self.Team)


Base.metadata.create_all(bind=engine)

session = sessionmaker()
session.configure(bind=engine)
my_session = session()


def get_all_players() -> List[str]:
    return my_session.query(Player).all()


def add_player(player: Player) -> None:
    my_session.add(player)
    my_session.commit()


def add_players(players_list: List[str]) -> None:
    my_session.add_all(players_list)
    my_session.commit()


def remove_player(player: Player) -> None:
    my_session.delete(player)
    my_session.commit()


def remove_all_players() -> None:
    my_session.execute("DELETE FROM players")
    my_session.commit()


def get_players_by_age_and_pot() -> List[str]:
    return my_session.query(Player).order_by(Player.Age.asc(), Player.Pot.desc()).limit(10)


players = []
players.append(Player(Name='Alex', Country='Romania', Age=22, Ovr=92, Pot=95))
players.append(Player(Name='Andrei', Country='Romania', Age=22, Ovr=90, Pot=95))
players.append(Player(Name='Alin', Country='Romania', Age=28, Ovr=91, Pot=94))
players.append(Player(Name='Tudor', Country='Romania', Age=31, Ovr=94, Pot=95))
players.append(Player(Name='Vasile', Country='Romania', Age=50, Ovr=88, Pot=93))
players.append(Player(Name='CR7', Country='Portugal', Age=33, Ovr=95, Pot=97))
players.append(Player(Name='Messi', Country='Argentina', Age=31, Ovr=95, Pot=97))
players.append(Player(Name='Ramos', Country='Spain', Age=33, Ovr=91, Pot=93))
players.append(Player(Name='Marcelo', Country='Brazil', Age=30, Ovr=89, Pot=92))
players.append(Player(Name='Neymar', Country='Brazil', Age=28, Ovr=92, Pot=95))
players.append(Player(Name='Mbappe', Country='France', Age=20, Ovr=89, Pot=95))
players.append(Player(Name='Ronaldinho', Country='Brazil', Age=37, Ovr=95, Pot=99))
players.append(Player(Name='Ronaldo', Country='Brazil', Age=40, Ovr=94, Pot=95))
players.append(Player(Name='Aguero', Country='Argentina', Age=30, Ovr=90, Pot=94))
players.append(Player(Name='Ibra', Country='Sweden', Age=35, Ovr=90, Pot=95))

remove_all_players()
add_players(players)
for i in get_all_players():
    print(i.Name)
print('-----------------------')
for y in get_players_by_age_and_pot():
    print(y.Name, y.Age, y.Pot)

my_session.close()
