# setup.py

from setuptools import setup, find_packages

setup(
    name='quantifyindia',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'nsetools',
        'requests',
    ],
    description='A package for fetching real-time and historical stock data from NSE and Alpha Vantage',
    author='Parth Chauhan',
    author_email='cparth495@gmail.com',
    url='https://github.com/Parthchauh/quantifyindia',
)
