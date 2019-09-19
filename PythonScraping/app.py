from PythonScraping.bsoup import get_search_results, get_modules_example
from PythonScraping.main import get_search_text_args, print_modules_example


search_text = get_search_text_args()
search_results = get_search_results(search_text=search_text)
modules_example = get_modules_example(modules=search_results)
print_modules_example(modules_example=modules_example)
