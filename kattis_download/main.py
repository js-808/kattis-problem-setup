#!/usr/bin/env python

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from os import name, path, makedirs
from requests import get
from sys import argv
from time import sleep
from urllib import request


url = "https://open.kattis.com/problems/"

# All Kattis accepted languages and correlated file extensions
LANGUAGES = {
    "apl": ".apl",
    "bash": ".sh", 
    "c": ".c",
    "c#": ".cs",
    "c++": ".cc",
    "cobol": ".cob",
    "lisp": ".lisp",
    "dart": ".dart",
    "f#": ".fs",
    "fortran": ".f90",
    "gerbil": ".ss",
    "go": ".go",
    "haskell": ".hs",
    "java": ".java",
    "javascript": ".js",
    "spidermonkey": ".js",
    "julia": ".jl",
    "kotlin": ".kt",
    "ocaml": ".ml", 
    "objective-c": ".m", 
    "php": ".php", 
    "pascal": ".pas",
    "prolog": ".pl", 
    "python2": ".py",
    "python3": ".py",
    "python": ".py",
    "ruby": ".rb", 
    "rust": ".rs",
    "typescript": ".ts",
    "visual-basic": ".vb"
}


def get_soup(problem: str) -> BeautifulSoup:
    """
    Scrape a Kattis page, specified by a problem ID, and return
    a parsed BeautifulSoup object.
    :param problem: A string Problem ID from Kattis
    :return A BeautifulSoup object
    """
    return BeautifulSoup(get(url + problem).text.strip(), "html.parser")


def parse_soup(soup: BeautifulSoup) -> dict:
    """
    Scrape a Kattis page, specified by a problem ID, and return
    a parsed BeautifulSoup object.
    :param problem: A string Problem ID from Kattis
    """
    assert valid_problem(soup), "Problem not found."

    # Parse into a dictionary
    p = dict()

    # Store the actual title of the problem
    p["title"] = soup.find("h1").text

    # Get the cpu time limit, memory limit, and difficulty of the problem 
    metadata = soup.find_all("div", {"class":"metadata_list-item"})
    tag_attr_name_mapping = {'cpu_limit':'cpu',
                     'mem_limit':'memory', 
                     'difficulty':'difficulty'}
    for item in metadata:
        try:
            data_name = item.attrs['data-name'].split('-')[1]
            if data_name in tag_attr_name_mapping:
                children = item.findChildren('span')
                p[tag_attr_name_mapping[data_name]] = children[-1].text
        except:
            pass

    # Find all tables with sample data in the Soup
    tables = soup.findAll("table", {"summary": "sample data"})
    p["tables"] = []
    for table in tables:
        p["tables"].append([j.text for j in table.findAll("pre")])

    return p


def valid_problem(soup: BeautifulSoup) -> bool:
    """
    Determine whether a given soup file is that of a valid Kattis problem.
    :param soup: A BeautifulSoup object parsed from a Kattis page
    :return True if the soup is that of a valid problem, False otherwise
    """

    # Easily tell - The title reads "404: Not Found" on a non-problem page
    return soup.find("h1").text != "404: Not Found"



def write_sample_data(dir: str, tables: list):
    """
    Write a list of sample data tables to file
    :param tables: A list of lists, each sublist being [input, answer] text
    """

    # Create target directory if not found
    if not path.isdir(dir):
        makedirs(dir)

    # Write each table to separate pair of files
    for i in range(len(tables)):

        # Write the input
        with open(dir + "/" + "sample" + str(i+1), "w") as f:
            f.write(tables[i][0])

        # Write the output
        with open(dir + "/" + "sample" + str(i+1) + "_ans", "w") as f:
            f.write(tables[i][1])

def create_empty_code_file(dir: str, prob_id: str, lang: str):
    """Create an empty code file with a given name and appropriate language extension.

    :param dir: The directory to write the new code file to 
    :param prob_id: The Kattis problem id 
    :param lang: The programming language 
    """
    # Check if language is valid
    lang_ = lang.lower()
    if lang_ not in LANGUAGES:
        raise ValueError(f"lang {lang} not valid language")

    # If valid, proceed to create the appropriate code file 
    # (if the file already exists, then don't overwrite it)
    ext = LANGUAGES[lang_]
    if not path.isdir(dir):
        makedirs(dir)
    new_file = path.join(dir, f'{prob_id}{ext}')
    with open(new_file, 'a'): pass 


def run():
    """
    Returns a list of problem data dictionaries if multiple problems are given, just the single dictionary if only one is given.
    """

    parser = ArgumentParser(prog="kattis-download")

    parser.add_argument('problems', metavar="N", nargs='+', help="name(s) of problem IDs on Kattis")
    parser.add_argument('-w', dest="write", action="store_const", const=True, default=False,
                        help="write data to a directory with same name as problem")
    parser.add_argument('-l', '--language', dest='language', 
                        choices=list(LANGUAGES),
                        help="create empty code file of the given language with the same name as the problem \
                            (`-w` flag must be set for this argument to have any effect).\
                            Allowed values are " + ', '.join(list(LANGUAGES)),
                        metavar='')

    if len(argv) < 2:
        parser.print_help()
        exit(0)

    namespace = parser.parse_args()

    problem_data = []

    for i, problem in enumerate(namespace.problems, start=1):

        print("Parsing:", problem, "\n")

        # Get the page and convert to Soup
        page = get_soup(problem)

        # Detect if it's a valid problem
        if not valid_problem(page):
            print(problem, "is not a valid Problem ID.")
            continue

        # Parse the title / sample data / CPU Time / Memory / Difficulty
        parsed = parse_soup(page)

        # Print information as a confirmation
        print("Title:", parsed["title"])
        print("ID:", problem)
        print("CPU Time Limit:", parsed["cpu"])
        print("Memory Limit:", parsed["memory"])
        print("Difficulty:", parsed["difficulty"], "\n")

        # Write the sample data to files
        # and create empty code file of appropriate language (if specified)
        if namespace.write:
            if "tables" in parsed:
                print("Writing sample data.")
                write_sample_data(problem, parsed["tables"])
            if namespace.language is not None:
                try:
                    print("Creating empty code file.")
                    create_empty_code_file(problem, problem, namespace.language)
                except ValueError as e:
                    print(f'ERROR: {e}. Continuing without creating code file . . .')

        problem_data.append(parsed)

        # Rate limit a bit
        if i % 10 == 0:
            sleep(5)

    return problem_data[0] if len(problem_data) == 1 else problem_data


if __name__ == "__main__":
    run()
