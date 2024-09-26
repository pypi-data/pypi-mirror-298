"""
Setup configuration file
"""
from setuptools import setup, find_packages

setup(
    name='get_looker_data',
    packages=find_packages(),
    package_data={'vacolba_looker_data': ['looker_studio/*', 'utils/*', 'utils/looker_studio/*', 'utils/webdriver/*']},
    include_package_data=True,
    version='1.0.6',
    description='General functions for the implementation of looker studio data.',
    authors=[
        {"name": "Rene Gonzalez Ramos", "email": "rgramos9310@gmail.com"}
    ],
    license="GPLv3",
    url="https://github.com/rgramos/vacolba-looker-data.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    entry_points={
        "flask.commands": [
            'generate-deploy = vacolba_looker_data.deploy:generate'
        ]
    }
)
