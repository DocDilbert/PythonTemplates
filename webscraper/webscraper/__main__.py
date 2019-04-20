import logging
import os
import sys
import re
import json
import argparse
import requests

from urllib.parse import urlparse, urlunparse

import webscraper.sqlliteblob as sqlliteblob
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
    response_raw = requests.get(request.get_url(), headers=HEADERS)
    
    module_logger.info("Request %s completed", request)
    log_raw_response(response_raw)

    response = Response(
        status_code = response_raw.status_code,
        content_type = response_raw.headers['Content-Type']
    )
    response_content = ResponseContent(content = response_raw.content)

    return (response, response_content)

def log_banner():
    module_logger.info("-------------------------------------")
    module_logger.info(" Web scrapper session startet")
    module_logger.info("-------------------------------------")

def init_logger(config_file):
    logger = logging.getLogger('webscraper')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    fh = logging.FileHandler(config_file, mode='w')
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s]: %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)


class WebScraperCommandLineParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="webscraper", 
            description='',
            usage=("webscraper config_file <command> [<args]\n"
                   "\n"
                   "The following commands are supported:\n"
                    "   sql     Stores content into the database.\n"
                    "   slist   Shows a list of stored sessions.\n")
        )

        # optional arguments:
        parser.add_argument(
            dest="config_file",
            type=str, 
            help='A configuration file in json format.'
        )
        parser.add_argument(
            'command', 
            help='Subcommand to run')

        args = parser.parse_args(sys.argv[1:3])
     
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def slist(self):
        config_file = sys.argv[1]
        parser = argparse.ArgumentParser(
            description='Stores web content into a database'
        )

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        _ = parser.parse_args(sys.argv[3:])

        with open(config_file) as json_data:
            config = json.load(json_data)

        init_logger(config['logfile'])
        connection =  sqlliteblob.create_or_open_db(config['database'])
        cursor = connection.cursor()
        sessions=sqlliteblob.list_all_sessions(cursor)
        for session in sessions:
            sid = session['id']
            session_obj = session['session']
            print("{:4} -- delta = {}  start = {}  end = {}".format(
                sid, 
                session_obj.get_delta_time(), 
                session_obj.start_datetime, 
                session_obj.end_datetime))

    def sql(self):
        config_file = sys.argv[1]
        parser = argparse.ArgumentParser(
            description='Stores web content into a database'
        )

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        _ = parser.parse_args(sys.argv[3:])

        with open(config_file) as json_data:
            config = json.load(json_data)
        
        init_logger(config['logfile'])
        log_banner()

        #content_handler = ContentHandlerFilesystem("page")
        content_handler_logger = ContentHandlerLogger()
        content_handler_sqlite = ContentHandlerSqlite(config['database'])

        content_handler_sqlite.set_component(content_handler_logger)
  
        links = webscraper(
            url = config['url'], 
            request_to_response = response_factory, 
            content_handler = content_handler_sqlite, 
            download_img = True
        )

        for link in links:
            parts=urlparse(link)
            filename = os.path.basename(parts.path)
            filen = os.path.splitext(filename)

            if filen[1]==".html":
                print(link)
                #scrap(link, scraper)
    
    def extract(self):
        config_file = sys.argv[1]
        parser = argparse.ArgumentParser(
            description='Extract web content from database'
        )

        # prefixing the argument with -- means it's optional
        parser.add_argument('session_id', type=int)

        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        _ = parser.parse_args(sys.argv[3:])

        with open(config_file) as json_data:
            config = json.load(json_data)
        
        init_logger(config['logfile'])
        log_banner()

        connection =  sqlliteblob.create_or_open_db(config['database'])
        cursor = connection.cursor()
        

def main():
    WebScraperCommandLineParser()


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    module_logger.exception("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

if __name__ == "__main__":
    
    # Install exception handler
    sys.excepthook = handle_exception

    main()