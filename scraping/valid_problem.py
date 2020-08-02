from bs4 import BeautifulSoup


def valid_problem(soup: BeautifulSoup) -> bool:
    """
    Determine whether a given soup file is that of a valid Kattis problem.
    :param soup: A BeautifulSoup object parsed from a Kattis page
    :return True if the soup is that of a valid problem, False otherwise
    """

    # Easily tell - The title reads "404: Not Found" on a non-problem page
    return soup.find("h1").text != "404: Not Found"
