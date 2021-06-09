from pathlib import Path
from setuptools import setup
from os import environ

cwd = Path(".")

README = (cwd / "README.md").read_text()
dependencies = (cwd / "requirements.txt").read_text().strip().split("\n")

# This should be set by the automated Github workflow
VERSION = environ["SEMANTIC_VERSION"]

setup(
    name="kattis-problem-setup",
    version=VERSION,
    description="View information on Kattis problems and download sample data.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/bradendubois/kattis-problem-setup",
    author="Braden Dubois",
    author_email="braden.dubois@usask.ca",
    packages=["kattis_download"],
    keywords="kattis parsing beautifulsoup",
    include_package_data=True,
    install_requires=dependencies,
    entry_points={
        'console_scripts': ["kattis-download=kattis_download.main:run"],
    }
)