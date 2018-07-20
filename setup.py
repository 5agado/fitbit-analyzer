from setuptools import setup, find_packages


setup(
    name="fitbit_scraper",
    version="0.1.0",
    description="Utility to scrape personal Fitbit data",
    license="Apache 2.0",
    author="Alex Martinelli",
    packages=find_packages(),
    entry_points={
        'console_scripts': ['fitbit-scraper=src.util.scraper:main'],
    },
    install_requires=[
        'fitbit',
        'cherrypy'
    ],
)
