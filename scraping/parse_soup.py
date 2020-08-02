from bs4 import BeautifulSoup
from requests import get
from urllib import request

from scraping.valid_problem import valid_problem

url = "https://open.kattis.com/problems/"


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
