from setuptools import find_packages, setup

from calculator import AUTHOR_EMAIL, AUTHOR_NAME, DESCRIPTION, NAME, VERSION


setup(
    # info
    name=NAME,
    description=DESCRIPTION,
    license='MIT',
    keywords=['film/substrate structure', 'stress calculator', 'cur'],

    # version
    version=VERSION,

    # author details
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,

    # setup directories
    packages=find_packages(),

    # setup data
    package_data={
        '': ['*.txt', '*.xml', '*.csv', '*.md'],
    },

    # requires
    install_requires=[
        item.strip() for item in open('requirements.txt', 'r').readlines()
        if item.strip()
    ],
    python_requires='>=3.11',
)
