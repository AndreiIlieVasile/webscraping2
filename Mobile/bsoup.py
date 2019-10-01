import re
import time
from typing import List, Dict
from typing import Optional

from bs4 import BeautifulSoup
from selenium import webdriver

from Mobile.alchemy import Car, convert_str_to_date

MAKE_MODEL_SOURCE = 'https://suchen.mobile.de/fahrzeuge/search.html?vc=Car&dam=0&lang=en'
ANY_MAKE_ID = 1400
ANY_MODEL_ID = 1


def get_make_id(make_name: str) -> int:
    """
    Returns the make's id from the site
    :param make_name: The make's name
    :return: An int representing the id
    """
    browser = webdriver.Chrome()
    browser.get(MAKE_MODEL_SOURCE)
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    browser.quit()

    ids_list = soup.find('select', id='selectMake1-ds')
    result_make_id = [make_id.get('value') for make_id in ids_list.find_all('option')
                      if (make_id.text == make_name)]
    if not result_make_id:
        return ANY_MAKE_ID
    return result_make_id[0]


def get_model_id(make_id: int, model_name: str) -> int:
    """
    Returns the model's id from the site
    :param make_id: The make's id
    :param model_name: The model's name
    :return: An int representing the model's id
    """
    browser = webdriver.Chrome()
    browser.get(MAKE_MODEL_SOURCE)
    xpath = f"//*[@id='selectMake1-ds']/option[@value='{make_id}']"
    browser.find_element_by_xpath(xpath).click()
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    browser.quit()

    ids_list = soup.find('select', id='selectModel1-ds')
    result_model_id = [model_id.get('value') for model_id in ids_list.find_all('option')
                       if (model_id.text.strip() == model_name)]
    if not result_model_id:
        return ANY_MODEL_ID
    return result_model_id[0]


def get_car_description(car_div: BeautifulSoup) -> str:
    """
    Returns a car's description
    :param car_div: The div which contains the description
    :return: A string representing the car's description
    """
    return car_div.find('div', class_='g-col-8').text


def get_car_price(car_div: BeautifulSoup) -> int:
    """
    Returns a car's price
    :param car_div: The div which contains the description
    :return: An int representing the car's price
    """
    price_data = car_div.find('span', class_='h3 u-block').text.strip('€')
    price_data = price_data.replace(',', '')
    return int(price_data)


def get_car_fr_mileage(car_div: BeautifulSoup) -> Dict:
    """
    Returns the first registration date and mileage of a car
    :param car_div: The div which contains the description
    :return: A dictionary containing the first registration date and the mileage
    """
    car_data = car_div.find('div', class_='rbt-regMilPow').text
    car_fr_mileage = {}

    fr_pattern = re.compile(r'FR\s([0-9]{2}/[0-9]{4})')
    fr = fr_pattern.search(car_data)
    if fr:
        fr = fr_pattern.search(car_data)[1]
        fr_date = convert_str_to_date(string=fr, format='%m/%Y')
        car_fr_mileage['fr_date'] = fr_date

    mileage_pattern = re.compile(r',\s([0-9]*\.[0-9]*)\skm')
    mileage = mileage_pattern.search(car_data)
    if mileage:
        mileage = mileage_pattern.search(car_data)[1]
        car_fr_mileage['mileage'] = mileage
    return car_fr_mileage


def get_car_chase_fuel_transmission(car_div: BeautifulSoup) -> Dict:
    """
    Returns the chase type, fuel type and transmission of a car
    :param car_div: The div which contains the description
    :return: A dictionary containing the chase_type, fuel_type and transmission
    """
    car_data = car_div.find('div', class_='rbt-regMilPow').findNext('div').text
    car_data = car_data.split(',')
    car_chase_fuel_transmission_dict = {}
    if car_data[0]:
        car_chase_fuel_transmission_dict['chase_type'] = car_data[0]
    if len(car_data) > 2 and ' Accident-free' not in car_data:
        car_chase_fuel_transmission_dict['fuel_type'] = car_data[1]
        car_chase_fuel_transmission_dict['transmission'] = car_data[2]
    if len(car_data) > 3:
        car_chase_fuel_transmission_dict['fuel_type'] = car_data[2]
        car_chase_fuel_transmission_dict['transmission'] = car_data[3]
    return car_chase_fuel_transmission_dict


def get_car_co2_emissions(car_div: BeautifulSoup) -> Optional[str]:
    """
    Returns the co2 emissions of a car
    :param car_div: The div which contains the description
    :return: A dictionary containing the co2 emissions
    """
    car_data = car_div.find('div', class_='vehicle-data--ad-with-price-rating-label').text
    co2_pattern = re.compile(r'([0-9]*)\sg\sCO', flags=re.UNICODE)
    match = co2_pattern.search(car_data)
    if match:
        return match[1]
    return None


def get_car_list_selenium(make_name: str, model_name: str, min_fr: int, max_fr: int) -> List[Car]:
    """
    Returns a list of cars with a given make and model and first registration date between an interval
    :param make_name: The make's name
    :param model_name: The model's name
    :param min_fr: The min first registration date
    :param max_fr: The max first registration date
    :return: A list of Car objects
    """
    make_id = get_make_id(make_name=make_name)
    if make_id == ANY_MAKE_ID:
        make_name = 'Other'
    model_id = get_model_id(make_id=make_id, model_name=model_name)
    if model_id == ANY_MODEL_ID:
        model_name = 'Other'

    source = f'https://suchen.mobile.de/fahrzeuge/search.html?damageUnrepaired=NO_DAMAGE_UNREPAIRED' \
             f'&isSearchRequest=true&lang=en&makeModelVariant1.makeId={make_id}&makeModelVariant1.modelId={model_id}' \
             f'&maxFirstRegistrationDate={max_fr}&maxPowerAsArray=PS&minFirstRegistrationDate={min_fr}' \
             f'&minPowerAsArray=PS&scopeId=C&sfmr=false'
    browser = webdriver.Chrome()
    browser.get(source)
    time.sleep(5)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    browser.quit()

    cars_list = []
    for car_div in soup.find_all('div', class_='g-col-9'):
        if car_div.findChildren('div', class_='g-row', recursive=False):
            car_description = get_car_description(car_div=car_div)
            car_price = get_car_price(car_div=car_div)

            car_fr_mileage = get_car_fr_mileage(car_div=car_div)
            car_fr_date = car_fr_mileage.get('fr_date', None)
            car_mileage = car_fr_mileage.get('mileage', None)

            car_chase_fuel_transmission = get_car_chase_fuel_transmission(car_div=car_div)
            car_chase_type = car_chase_fuel_transmission.get('chase_type', None)
            car_fuel_type = car_chase_fuel_transmission.get('fuel_type', None)
            car_transmission = car_chase_fuel_transmission.get('transmission', None)

            car_co2_emissions = get_car_co2_emissions(car_div=car_div)

            cars_list.append(
                Car(make=make_name, model=model_name, description=car_description, price=car_price,
                    fr_date=car_fr_date, mileage=car_mileage, chase_type=car_chase_type,
                    fuel_type=car_fuel_type, transmission=car_transmission, co2_emissions=car_co2_emissions)
            )
    return cars_list
