import logging
import os
import re
import json
import argparse
from urllib.parse import urlparse, urlunparse

from webscraper.webscraper import webscraper 
from webscraper.content_handler_sqlite import ContentHandlerSqlite
from webscraper.content_handler_logger import ContentHandlerLogger
from webscraper.content_handler_filesystem import ContentHandlerFilesystem

def main():

    parser = argparse.ArgumentParser(prog="webscraper", description='Web scraper')

    # optional arguments:
    parser.add_argument(
        dest="config_file",
        type=str, 
        help='A configuration file in json format.'
    )

    args = parser.parse_args()
    with open(args.config_file) as json_data:
        config = json.load(json_data)


    
    logger = logging.getLogger('webscraper')
    logger.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    fh = logging.FileHandler(config['logfile'], mode='w')
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s]: %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("-------------------------------------")
    logger.info(" Web scrapper session startet")
    logger.info("-------------------------------------")

    content_handler = ContentHandlerFilesystem("page")
    content_handler_logger = ContentHandlerLogger()
    content_handler_sqlite = ContentHandlerSqlite(config['database'])

    content_handler_sqlite.set_component(content_handler_logger)
    content_handler.set_component(content_handler_sqlite)

    links = webscraper(config['url'], content_handler, download_img=True)

    for link in links:
        parts=urlparse(link)
        filename = os.path.basename(parts.path)
        filen = os.path.splitext(filename)

        if filen[1]==".html":
            print(link)
            #scrap(link, scraper)

if __name__ == "__main__":
    main()