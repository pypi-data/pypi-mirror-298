# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aima', 'aima.hobs']

package_data = \
{'': ['*'], 'aima': ['images/*']}

install_requires = \
['cvxopt',
 'image',
 'ipython',
 'ipythonblocks',
 'ipywidgets',
 'keras',
 'matplotlib',
 'networkx',
 'numpy',
 'opencv-python',
 'pandas',
 'pillow',
 'pytest-cov',
 'qpsolvers',
 'scipy',
 'sortedcontainers',
 'tensorflow']

entry_points = \
{'console_scripts': ['aima = aima.main:main']}

setup_kwargs = {
    'name': 'aima',
    'version': '2024.9.27',
    'description': 'Artificial Intelligence a Modern Approach 4th Ed by Peter Norvig and Stuart Russel',
    'long_description': "# Introduction\n\nCode for Artificial Intelligence: A Modern Approach (AIMA) 4th edition by Peter Norvig and Stuart Russel.\n\nShameless reuse of Norvig's official repository at https://github.com/aimacode/aima-python/ \n\nThe code should work in Python 3.9 and Python 3.10. Not yet tested with Python 3.11, 3.12, or 3.13.\n\n# Browse\n\nYou can get some use out of the code here just by browsing, starting at the root of the source tree or by clicking on the links in the index on the project home page. The source code is in the .py files; the .txt files give examples of how to use the code.\n\n## Installation\n\n#### Linux\n```bash\ngit clone git@gitlab.com:tangibleai/inactive/aima\ncd aima\npython3.10 -m venv .venv\nsource .venv/bin/activate \npip install -e .\n```\n\n#### Mac\n1. install XCode\n2. use Linux instructions above\n\n#### Windows\n1. install git-bash or WSL\n2. use Linux instruction above\n\n## Testing\n\nIn the `aima/` directory, execute the command\n\n```bash\npython doctests.py -v *.py\n```\n\n## Run the Code\n\nYou're on your own -- experiment!\nRead the book, create a new python file, import the modules you need, and call the functions you want!\n\n## Acknowledgements\n\nNorvig and the aima-python contibutors:\nMany thanks for the bug reports, corrected code, and other support from Phil Ruggera, Peng Shao, Amit Patil, Ted Nienstedt, Jim Martin, Ben Catanzariti, and others.\n",
    'author': 'Peter Norvig (norvig)',
    'author_email': 'peter.norvig@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/tangibleai/community/aima',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
