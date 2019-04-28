from distutils.core import setup
from version import __version__

setup(
    name='webscraper',
    version=__version__,
    packages=['webscraper', 'webdb', 'webtypes','version', ],
    long_description=open('README.txt').read(),
    #data_files=['VERSION'],
    
    # Setuptools allows modules to register entrypoints which other 
    # packages can hook into to provide certain functionality. 
    # It also provides a few itself, including the console_scripts entry point.
    entry_points = {
        'console_scripts': ['webscraper=webscraper.__main__:main'],
    }
)