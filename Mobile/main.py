import argparse
from typing import Dict

from Mobile.alchemy import get_all_cars, add_cars, get_avg_price, close_session
from Mobile.bsoup import get_car_list_selenium

# from Mobile.alchemy import remove_all_cars
# remove_all_cars()


def get_search_args() -> Dict:
    """
    Gets the make, model, min and max first registration dates arguments
    :return: The dictionary containing the arguments
    """
    parser = argparse.ArgumentParser(description='Gets the arguments needed for a search')
    parser.add_argument('-ma', '--make', type=str, required=True, help="The make of the car.")
    parser.add_argument('-mo', '--model', type=str, required=True, help="The model of the car.")
    parser.add_argument('-minfr', '--minfirstregistration', type=int, required=True,
                        help="The minimum first registration year.")
    parser.add_argument('-maxfr', '--maxfirstregistration', type=int, required=True,
                        help="The maximum first registration year.")
    args = parser.parse_args()
    args_dict = {
        'make': args.make,
        'model': args.model,
        'min_fr': args.minfirstregistration,
        'max_fr': args.maxfirstregistration
    }
    return args_dict


args_dict = get_search_args()


cars_list = get_car_list_selenium(make_name=args_dict['make'], model_name=args_dict['model'],
                                  min_fr=args_dict['min_fr'], max_fr=args_dict['max_fr'])
add_cars(cars_list=cars_list)

# print(*get_all_cars(), sep='\n')


average = get_avg_price(make_name=args_dict['make'], model_name=args_dict['model'],
                        min_fr_int=args_dict['min_fr'], max_fr_int=args_dict['max_fr'])
print(average)

close_session()
