from bs4 import BeautifulSoup
from requests import get
from urllib import request

url = "https://open.kattis.com/problems/"


def parse_soup(soup: BeautifulSoup) -> dict:
    """
    Scrape a Kattis page, specified by a problem ID, and return 
    a parsed BeautifulSoup object.
    :param problem: A string Problem ID from Kattis
    """
    print(soup.findAll("table", {"summary": "sample data"}))
