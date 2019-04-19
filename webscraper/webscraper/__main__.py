import logging
import os
import re
import json
import argparse
import requests
from urllib.parse import urlparse, urlunparse

from webscraper.webscraper import webscraper 
from webscraper.content_handler_sqlite import ContentHandlerSqlite
from webscraper.content_handler_logger import ContentHandlerLogger
from webscraper.content_handler_filesystem import ContentHandlerFilesystem
from webscraper.request import Request
from webscraper.response import Response
from webscraper.response_content import ResponseContent

#chrome 70.0.3538.77
HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

# create logger
module_logger = logging.getLogger('webscraper')



def log_raw_response(response):
    module_logger.debug("Raw response received:\n"
        "\tstatus_code = %s,\n"
        "\theaders = %s,\n"
        "\tcookies = %s,\n"
        "\tencoding = %s",response.status_code, response.headers, response.cookies, response.encoding)

def response_factory(request):
    response_raw = requests.get(request.to_url(), headers=HEADERS)
    
    module_logger.info("Request %s completed", request)
    log_raw_response(response_raw)

    response = Response(
        status_code = response_raw.status_code,
        content_type = response_raw.headers['Content-Type']
    )
    response_content = ResponseContent(content = response_raw.content)

    return (response, response_content)

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

    links = webscraper(
        config['url'], 
        response_factory, 
        content_handler, 
        download_img=True
    )

    for link in links:
        parts=urlparse(link)
        filename = os.path.basename(parts.path)
        filen = os.path.splitext(filename)

        if filen[1]==".html":
            print(link)
            #scrap(link, scraper)

if __name__ == "__main__":
    main()