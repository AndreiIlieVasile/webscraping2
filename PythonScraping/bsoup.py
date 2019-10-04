import re
import time
from typing import List, Dict

from bs4 import BeautifulSoup
from selenium import webdriver


def get_search_results(search_text: str) -> List[str]:
    """
    Gets the module links from the result of a searc
    :param search_text: The text to search for
    :return: A list of strings containing the module links from the result of a search
    """
    source = f'https://docs.python.org/3.6/search.html?q={search_text}&check_keywords=yes&area=default'
    browser = webdriver.Chrome()
    browser.get(source)
    time.sleep(5)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    browser.quit()

    search_ul = soup.find('ul', class_='search')
    return [i.a.text for i in search_ul.find_all('li', limit=100)
            if i.a.findChildren('code')]


def get_all_modules() -> List[str]:
    """
    Gets all the modules names
    :return: - A list of strings containing all the modules names
    """
    source = 'https://docs.python.org/3.6/py-modindex.html'
    browser = webdriver.Chrome()
    browser.get(source)
    time.sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    browser.quit()

    modules_table = soup.find('table', class_='indextable modindextable')
    return [i.a.text for i in modules_table.find_all('td')
            if i.a]


def get_modules_example(modules: List[str]) -> Dict:
    """
    Gets the first example for each module
    :param modules: A list of modules links
    :return: A dictionary containing the first example for each module
    """
    modules_example = {}
    all_modules = get_all_modules()

    for module_link in modules:
        pattern = re.compile(r'\.\s([a-z.]*)\s')
        match = pattern.search(module_link)
        if not match:
            continue

        module_short = match[1]
        if module_short not in all_modules:
            continue
        source = f'https://docs.python.org/3.6/library/{module_short}.html?highlight=scheduler'
        browser = webdriver.Chrome()
        browser.get(source)
        time.sleep(2)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')
        browser.quit()

        example = soup.find('pre')
        if example is not None:
            modules_example[module_short] = example.text
        else:
            example = f'Could not find any examples for: {module_short} module'
            modules_example[module_short] = example
    return modules_example
