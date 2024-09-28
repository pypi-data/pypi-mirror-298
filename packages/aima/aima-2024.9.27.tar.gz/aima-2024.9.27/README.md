# Introduction

Code for Artificial Intelligence: A Modern Approach (AIMA) 4th edition by Peter Norvig and Stuart Russel.

Shameless reuse of Norvig's official repository at https://github.com/aimacode/aima-python/ 

The code should work in Python 3.9 and Python 3.10. Not yet tested with Python 3.11, 3.12, or 3.13.

# Browse

You can get some use out of the code here just by browsing, starting at the root of the source tree or by clicking on the links in the index on the project home page. The source code is in the .py files; the .txt files give examples of how to use the code.

## Installation

#### Linux
```bash
git clone git@gitlab.com:tangibleai/inactive/aima
cd aima
python3.10 -m venv .venv
source .venv/bin/activate 
pip install -e .
```

#### Mac
1. install XCode
2. use Linux instructions above

#### Windows
1. install git-bash or WSL
2. use Linux instruction above

## Testing

In the `aima/` directory, execute the command

```bash
python doctests.py -v *.py
```

## Run the Code

You're on your own -- experiment!
Read the book, create a new python file, import the modules you need, and call the functions you want!

## Acknowledgements

Norvig and the aima-python contibutors:
Many thanks for the bug reports, corrected code, and other support from Phil Ruggera, Peng Shao, Amit Patil, Ted Nienstedt, Jim Martin, Ben Catanzariti, and others.
