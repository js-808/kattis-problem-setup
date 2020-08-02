from bs4 import BeautifulSoup
from os import path, makedirs

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
