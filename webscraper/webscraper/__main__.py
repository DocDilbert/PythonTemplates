import logging
import logging.handlers as handlers
import os
import sys
import re
import json
import argparse
import requests

from urllib.parse import urlparse, urlunparse

import sqliteblob.sqliteblob as sqliteblob
from webscraper.webscraper import webscraper 
from webscraper.content_handler_sqlite import ContentHandlerSqlite
from webscraper.content_handler_logger import ContentHandlerLogger
from webscraper.content_handler_filesystem import ContentHandlerFilesystem
from webtypes.request import Request
from webtypes.response import Response
from webtypes.response_content import ResponseContent

from webscraper.version import (
    __version__,
)

#chrome 70.0.3538.77
HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

CONFIG_FILE_NAME = "webscraper.json"

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

    response = Response.fromGMT(
        status_code = response_raw.status_code,
        date_gmt = response_raw.headers['Date'],
        content_type = response_raw.headers['Content-Type']
    )
    RESPONSE_CONTENTS = ResponseContent(content = response_raw.content)

    return (response, RESPONSE_CONTENTS)

class RequestToDatabase:
    def __init__(self, cursor, session_id):
        self.session_id = session_id
        self.cursor = cursor

    def response_database_factory(self,request):
        response, RESPONSE_CONTENTS = sqliteblob.extract_response_by_request(
            self.cursor,
            self.session_id,
            request
        )
        
        module_logger.info("Request %s completed", request)
   
        return (response, RESPONSE_CONTENTS)


def log_banner():
    module_logger.info("-------------------------------------")
    module_logger.info(" Web scrapper session startet")
    module_logger.info("-------------------------------------")

def init_logger(config):
    logger = logging.getLogger('webscraper')
    logger.setLevel(logging.DEBUG)

    logger2 = logging.getLogger('sqliteblob')
    logger2.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    if config['logtype'] == "rotate":
        fh = handlers.RotatingFileHandler(config['logfile'], maxBytes=10*1024*1024, backupCount=10)
    else:
        fh = logging.FileHandler(config['logfile'], mode='w')
    
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s]: %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger2.addHandler(fh)
    logger2.addHandler(ch)


class WebScraperCommandLineParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="webscraper", 
            description='',
            usage=("webscraper <command> [<args]\n"
                   "\n"
                   "The following commands are supported:\n"
                   "   extract  Extract webpage by session id.\n"
                   "   sql      Stores content into the database.\n"
                   "   slist    Shows a list of stored sessions.\n"
                   "   info     Shows some useful info of the database.")
        )

        parser.add_argument(
            'command', 
            help='Subcommand to run')

        parser.add_argument('--version', action='version',
                    version='%(prog)s {version}'.format(version=__version__))
        args = parser.parse_args(sys.argv[1:2])
     
        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def slist(self):
        parser = argparse.ArgumentParser(
            prog="webscraper slist", 
            description='Stores web content into a database'
        )

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        _ = parser.parse_args(sys.argv[2:])

        with open(CONFIG_FILE_NAME) as json_data:
            config = json.load(json_data)

        init_logger(config)
        connection =  sqliteblob.create_or_open_db(config['database'])
        cursor = connection.cursor()
        sessions=sqliteblob.list_all_sessions(cursor)
        for session in sessions:
            sid = session['id']
            session_obj = session['session']
            print("{:4} -- delta = {}  start = {}  end = {}".format(
                sid, 
                session_obj.get_delta_time(), 
                session_obj.start_datetime, 
                session_obj.end_datetime))
        

    def info(self):
        parser = argparse.ArgumentParser(
            prog="webscraper info", 
            description='Stores web content into a database'
        )

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        _ = parser.parse_args(sys.argv[2:])

        with open(CONFIG_FILE_NAME) as json_data:
            config = json.load(json_data)

        init_logger(config)
        statinfo = os.stat(config['database'])
        connection =  sqliteblob.create_or_open_db(config['database'])
        cursor = connection.cursor()
        info = sqliteblob.info(cursor)
        content_size = sqliteblob.compute_content_size(cursor)
        print(
            "---------------------------------------------------------\n"
            "                            Session count: {}\n"
            "                            Request count: {}\n"
            "                           Response count: {}\n"
            "                    ResponseContent count: {}\n"
            "                              Cache ratio: {:.2f}\n"
            "---------------------------------------------------------\n"
            "        Average Request count per session: {:.1f}\n"
            "       Average Response count per session: {:.1f}\n"
            " Average ResponeContent count per session: {:.1f}\n"
            "---------------------------------------------------------\n"
            "                         Size of database: {:.1f} KB\n"
            "              Size of content in database: {:.1f} KB\n"
            "        Size of overhead data in database: {:.1f} KB\n"
            "                           Overhead ratio: {:.2f}\n"
            "                  Average size of session: {:.1f} KB\n"
            "---------------------------------------------------------"
            "".format(
                info['session_count'],
                info['request_count'],
                info['response_count'],
                info['RESPONSE_CONTENTS_count'],
                1-info['RESPONSE_CONTENTS_count']/info['response_count'],
                info['request_count']/info['session_count'],
                info['response_count']/info['session_count'],
                info['RESPONSE_CONTENTS_count']/info['session_count'],
                statinfo.st_size/1024,
                content_size/1024,
                (statinfo.st_size-content_size)/1024,
                (statinfo.st_size-content_size)/statinfo.st_size,
                statinfo.st_size/1024/info['session_count']
            ))

    def sql(self):
        parser = argparse.ArgumentParser(
            prog="webscraper sql", 
            description='Stores web content into a database'
        )

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        _ = parser.parse_args(sys.argv[2:])

        with open(CONFIG_FILE_NAME) as json_data:
            config = json.load(json_data)
        
        init_logger(config)
        log_banner()

        #content_handler = ContentHandlerFilesystem("page")
        content_handler_logger = ContentHandlerLogger()
        content_handler_sqlite = ContentHandlerSqlite(config['database'])

        content_handler_sqlite.set_component(content_handler_logger)
  
        regex = re.compile(config['link_filter'])
        webscraper(
            url = config['url'], 
            request_to_response = response_factory, 
            content_handler = content_handler_sqlite, 
            download_img = True,
            link_filter=lambda x: True if regex.match(x) else False,
            max_level=config['max_level']
        )
    
    def extract(self):
        parser = argparse.ArgumentParser(
            prog="webscraper extract", 
            description='Extract web content from database'
        )

        # prefixing the argument with -- means it's optional
        parser.add_argument('session_id', type=int)
        parser.add_argument('dirname', type=str)
        
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])

        with open(CONFIG_FILE_NAME) as json_data:
            config = json.load(json_data)
        
        init_logger(config)
        log_banner()

        connection =  sqliteblob.create_or_open_db(config['database'])
        cursor = connection.cursor()
        rtb = RequestToDatabase(cursor, args.session_id)

        content_handler_filesystem = ContentHandlerFilesystem(args.dirname)
        content_handler_logger = ContentHandlerLogger()
        content_handler_filesystem.set_component(content_handler_logger)
        regex = re.compile(config['link_filter'])
        
        webscraper(
            url = config['url'], 
            request_to_response = rtb.response_database_factory, 
            content_handler = content_handler_filesystem, 
            download_img = True,
            link_filter=lambda x: True if regex.match(x) else False,
            max_level=config['max_level']
        )
        
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