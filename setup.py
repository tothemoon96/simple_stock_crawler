# Automatically created by: scrapyd-deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '1.0',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = stock_price_crawler.settings']},
    package_data={
        '': ['*.yaml'],
    },
)
