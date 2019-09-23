import re
import os
import argparse

DIRECTORY = os.fsencode('/Users/andrei.ilie/PycharmProjects/webscraping2/REGEX')


def create_files() -> None:
    for i in range(0, 100):
        with open(f"text{i}.txt", "w") as f:
            f.write(f"Hello world {i}\n")
            f.write(f"{i} hello world\n")
            f.write(f"world {i} hello\n")
            f.write(f"wworld {i} hello\n")
            f.write(f"world{i} hello\n")
            f.write(f"{i}world hello\n")
            f.write(f"{i} worldworld hello\n")


def get_word() -> str:
    parser = argparse.ArgumentParser(description='Gets a string representing a word')
    parser.add_argument('-w', '--word', type=str, required=True, help="The word that you want to match.")
    args = parser.parse_args()
    return args.word


def get_pattern() -> re.Pattern:
    word = get_word()
    pattern = re.compile(r"[\s]" + word + r"[\s]")
    return pattern


def match_regex(pattern: re.Pattern, directory: bytes) -> None:
    for file in os.listdir(directory):
        filename = os.fsencode(file)
        if filename.endswith(b".txt"):
            with open(filename, 'r') as f:
                contents = f.read()
                matches = pattern.finditer(contents)
                for match in matches:
                    print(match.group(0))


match_regex(get_pattern(), DIRECTORY)
