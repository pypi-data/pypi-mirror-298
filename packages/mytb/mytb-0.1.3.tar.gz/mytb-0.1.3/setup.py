# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mytb',
 'mytb.aio',
 'mytb.commands',
 'mytb.file',
 'mytb.gitlab',
 'mytb.html',
 'mytb.importlib',
 'mytb.ipc',
 'mytb.logging',
 'mytb.logging.configs',
 'mytb.logging.handlers',
 'mytb.tests',
 'mytb.tests.gitlab']

package_data = \
{'': ['*']}

install_requires = \
['unidecode']

extras_require = \
{'all': ['dateutils', 'ddt', 'pytz', 'pyyaml', 'tzlocal'],
 'date': ['dateutils', 'pytz', 'tzlocal'],
 'gitlab': ['ddt', 'pyyaml']}

entry_points = \
{'console_scripts': ['mytb = mytb.commands:main']}

setup_kwargs = {
    'name': 'mytb',
    'version': '0.1.3',
    'description': 'my toolbox for everyday python projects',
    'long_description': "Welcome to MyTB (My Toolbox)\n\nMyTB is just another collection of handy and useful python functions and modules.\n\n\n.. image:: https://travis-ci.com/feenes/mytb.svg?branch=master\n    :target: https://travis-ci.com/feenes/mytb\n\n\nIt can be found at https://github.com/feenes/mytb.git\n\nIt tries to be modular in order to consume as little memory (RAM) as possible.\n\nGetting started\n===============\n\nInstallation\n------------\n\nWith pip ::\n\n    pip install mytb # basic installation with basic dependencies\n    pip install mytb[date] # with all dependencies for mytb.date\n    pip install mytb[gitlab] # with all dependencies for mytb.gitlab\n    pip install mytb[all] # with all dependencies\n\n    **!!version 0.1 is only python 3 compatible!!**\n    Use `pip install 'mytb<0.1'` to get the latest python2 compatible version\n\nWho's using mytb\n==================\n\nPlease contact us if you want to be referenced\n\nProjects, that I know of are\n\n    * MHComm ( https://mhcomm.fr ) for most of their python projects\n    * The timon project ( https://github.com/feenes/timon )\n\n",
    'author': 'Teledomic',
    'author_email': 'info@teledomic.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/feenes/mytb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
