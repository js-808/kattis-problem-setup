from bs4 import BeautifulSoup
from requests import get
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
