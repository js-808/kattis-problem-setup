from sys import argv

from scraping.get_soup import get_soup
from scraping.parse_soup import parse_soup
from scraping.valid_problem import valid_problem
from scraping.write_sample_data import write_sample_data

# Read all problem IDs from sys.argv
if len(argv) == 1:
    print("No problems specified.")
    exit(0)

# Handle each problem, one by one
for problem_id in argv[1:]:

    print("Parsing:", problem_id, "\n")

    # Get the page and convert to Soup
    page = get_soup(problem_id)

    # Detect if it's a valid problem
    if not valid_problem(page):
        print(problem_id, "is not a valid Problem ID.")
        continue

    # Parse the title / sample data / CPU Time / Memory / Difficulty
    parsed = parse_soup(page)

    # Print information as a confirmation
    print("Title:", parsed["title"])
    print("ID:", problem_id)
    print("CPU Time Limit:", parsed["cpu"])
    print("Memory Limit:", parsed["memory"])
    print("Difficulty:", parsed["difficulty"], "\n")

    # Write the sample data to files
    if "tables" in parsed:
        print("Writing sample data.")
        write_sample_data(problem_id, parsed["tables"])
