from bs4 import BeautifulSoup


def valid_problem(soup: BeautifulSoup) -> bool:
    return soup.find("h1").text != "404: Not Found"
