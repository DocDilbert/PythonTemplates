from distutils.core import setup

setup(
    name='webscraper',
    version='0.0.1',
    packages=['webscraper',],
    long_description=open('README.txt').read(),
    
    # Setuptools allows modules to register entrypoints which other 
    # packages can hook into to provide certain functionality. 
    # It also provides a few itself, including the console_scripts entry point.
    entry_points = {
        'console_scripts': ['webscraper=webscraper.__main__:main'],
    }
)