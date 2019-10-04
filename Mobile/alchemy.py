from datetime import datetime
from operator import attrgetter
from typing import List, Tuple, Any

from sqlalchemy import Column, String, Integer, Date
from sqlalchemy import create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///cars.db")

Base = declarative_base()


class Car(Base):
    """
    Class for car objects
    """
    __tablename__ = 'cars'
    id = Column(Integer(), primary_key=True)
    make = Column(String(40), nullable=False)
    model = Column(String(100), nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Integer())
    fr_date = Column(Date())
    mileage = Column(String(10))
    chase_type = Column(String(30))
    fuel_type = Column(String(30))
    transmission = Column(String(30))
    co2_emissions = Column(String(20))

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id}, make={self.make}, model={self.model}," \
               f" description={self.description}, price={self.price}, fr_date={self.fr_date}," \
               f" mileage={self.mileage}, chase_type={self.chase_type}, fuel_type={self.fuel_type}," \
               f" transmission={self.transmission}, co2_emissions={self.co2_emissions})"


Base.metadata.create_all(bind=engine)

session = sessionmaker()
session.configure(bind=engine)
my_session = session()


def get_all_cars() -> List[Car]:
    """
    :return: The list of cars from th db
    """
    return my_session.query(Car).all()


def get_min_max_fr_dates(cars_list: List[Car]) -> Tuple[Any, Any]:
    """
    Returns the min and max first registration_date from a list of cars
    :param cars_list: The cars list
    :return: A tuple with the min and max first registration date
    """
    cars_list_min_fr = min(cars_list, key=attrgetter('fr_date')).fr_date
    cars_list_max_fr = max(cars_list, key=attrgetter('fr_date')).fr_date
    return cars_list_min_fr, cars_list_max_fr


def add_cars(cars_list: List[Car]) -> None:
    """
    Inserts a list of cars in db, if there are no cars in the db with the same make, model and
     first registration date range between the min and max first registration range from the db
    :param cars_list: The cars list
    :return: -
    """
    if not cars_list:
        return
    min_list_fr_date, max_list_fr_date = get_min_max_fr_dates(cars_list=cars_list)
    min_db_fr_date = my_session.query(Car.fr_date, func.min(Car.fr_date)) \
        .filter(Car.make == cars_list[0].make, Car.model == cars_list[0].model).scalar()
    max_db_fr_date = my_session.query(Car.fr_date, func.max(Car.fr_date)) \
        .filter(Car.make == cars_list[0].make, Car.model == cars_list[0].model).scalar()

    if min_db_fr_date and max_db_fr_date:
        search = my_session.query(Car).filter(Car.make == cars_list[0].make, Car.model == cars_list[0].model,
                                              min_db_fr_date < min_list_fr_date
                                              < max_list_fr_date < max_db_fr_date).first()
        if search:
            return

    for car in cars_list:
        if my_session.query(Car).filter(Car.description == car.description, Car.price == car.price).first():
            continue
        my_session.add(car)
    my_session.commit()


def convert_str_to_date(string: str, format: str):
    """
    Converts a string into a date
    :param string: The string
    :param format: The format
    :return: The date result
    """
    date = datetime.strptime(string, format)
    return datetime.date(date)


def get_avg_price(make_name: str, model_name: str, min_fr_int: int, max_fr_int: int) -> str:
    """
    Returns the average price for a car with the first registration date between 2 given dates
    :param make_name: The make of the cars
    :param model_name: The model of the cars
    :param min_fr_int: An integer representing the min date
    :param max_fr_int: An integer representing the max date
    :return: The average price
    """
    min_fr_date = convert_str_to_date(string=str(min_fr_int), format='%Y')
    max_fr_date = convert_str_to_date(string=str(max_fr_int), format='%Y')

    avg = my_session.query(func.avg(Car.price)).filter(Car.make == make_name, Car.model == model_name,
                                                       min_fr_date < Car.fr_date, Car.fr_date < max_fr_date).all()
    avg = str(avg[0]).replace('(', '')
    avg = avg.replace(',', '')
    avg = avg.replace(')', '')
    return f'The average price for {make_name} {model_name} from {min_fr_int} to {max_fr_int} is: {avg}'


def remove_all_cars() -> None:
    """
    Removes all the cars from db
    :return: -
    """
    my_session.query(Car).delete()
    my_session.commit()


def close_session() -> None:
    """
    Closes the session
    :return: -
    """
    my_session.close()
