#!/usr/bin/env python

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from os import name, path, makedirs
from requests import get
from sys import argv
from time import sleep
from urllib import request


url = "https://open.kattis.com/problems/"


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

    # Nested "sidebar-info" divs; recursively move inwards until at deepest
    sidebar = soup.find("div", {"class": "sidebar-info"})
    while sidebar.find("div", {"class": "sidebar-info"}):
        sidebar = sidebar.find("div", {"class": "sidebar-info"})

    # Last level deep has 2, the first is the buttons, second is problem data
    sidebar = sidebar.find_next_sibling("div")

    # Take the value in each attribute, ignore first (ID)
    attributes = [p.text.split(":")[1].strip() for p in sidebar.findChildren("p")][1:]
    attribute_keys = ["cpu", "memory", "difficulty"]
    for _ in range(len(attribute_keys)):
        p[attribute_keys[_]] = attributes[_]

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


def run():
    """
    Returns a list of problem data dictionaries if multiple problems are given, just the single dictionary if only one is given.
    """

    parser = ArgumentParser(prog="kattis-download")

    parser.add_argument('problems', metavar="N", nargs='+', help="name(s) of problem IDs on Kattis")
    parser.add_argument('-w', dest="write", action="store_const", const=True, default=False,
                        help="write data to a directory with same name as problem")

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
        if "tables" in parsed and namespace.write:
            print("Writing sample data.")
            write_sample_data(problem, parsed["tables"])

        problem_data.append(parsed)

        # Rate limit a bit
        if i % 10 == 0:
            sleep(5)

    return problem_data[0] if len(problem_data) == 1 else problem_data


if __name__ == "__main__":
    run()
