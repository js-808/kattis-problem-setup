# kattis-problem-setup

Download the sample data for any problems from [Kattis](https://open.kattis.com/).

## Requirements

The project is built in [Python 3](https://www.python.org/).

## Installation

To install, simply clone the project:

```shell_script
git clone https://github.com/bradendubois/kattis-problem-setup
cd kattis-problem-setup
```

## Usage

To run the project, simply run the ``main.py`` either directly, or in Python, with any number of problem IDs provided.

```shell_script
./main.py PROBLEM_1 PROBLEM_1
```

or

```shell_script
python main.py PROBLEM_1 PROBLEM_2
```

where ``PROBLEM`` would be the ID of a problem. 

**Example**: If there were sample material for the problem [Hello World!](https://open.kattis.com/problems/hello), where the ID is ``hello``, usage would be:

```shell_script
pythom main.py hello
```

and output would be:

```
Parsing: hello 

Title: Hello World!
ID: hello
CPU Time Limit: 5 seconds
Memory Limit: 1024 MB
Difficulty: 1.2
```

## Disclaimers

**The description of each problem is not downloaded.**

Kattis [Terms of Service](https://open.kattis.com/help/tos) is clear (see ``2. License for content``); materials cannot be (a) *copied* or (b) *publically displayed*. This script gets uninformative information on memory limits / CPU time, etc. but does not represent materials concerning the *problem itself*. It would be a clear violation of the TOS to copy, or likely facilitate copying, the actual description of each problem. 

**Can it copy all the problems from Kattis?**

It could be easily made to download a description of every problem from Kattis, but for the same reasons as above, it will not be implemented.

## Acknowledgements

- [Kattis](https://open.kattis.com/), for hosting fun competitive programming problems.
- [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/), still the best choice for web scraping in Python.
