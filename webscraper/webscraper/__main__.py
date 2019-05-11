# -*- coding: utf-8 -*-

import logging
import logging.handlers as handlers
import os
import sys
import re
import json
import argparse
import requests
import time
from urllib.parse import urlparse, urlunparse

import webdb

from webscraper.webscraper import webscraper
from webscraper.content_handler_sqlite import ContentHandlerSqlite
from webscraper.content_handler_logger import ContentHandlerLogger
from webscraper.content_handler_filesystem import ContentHandlerFilesystem
from webtypes.request import Request
from webtypes.response import Response

from version import __version__

CRAWL_DELAY = 0 # 1 second delay per request
# chrome 70.0.3538.77
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

CONFIG_FILE_NAME = "webscraper.json"

# create logger
module_logger = logging.getLogger('webscraper')


def log_raw_response(response):
    module_logger.debug(
        "Raw response received:\n"
        "\tstatus_code = %s,\n"
        "\theaders = %s,\n"
        "\tcookies = %s,\n"
        "\tencoding = %s", response.status_code, response.headers, response.cookies, response.encoding
    )


def response_factory(request):
    module_logger.debug("Perfom web request %s", request)
    response_raw = requests.get(request.get_url(), headers=HEADERS)
    module_logger.info("Web request %s completed", request)

    module_logger.debug("Sleeping %i seconds... tzzz tzzz tzzz", CRAWL_DELAY)
    time.sleep(CRAWL_DELAY)
    
    log_raw_response(response_raw)

    response = Response.fromGMT(
        status_code=response_raw.status_code,
        date_gmt=response_raw.headers['Date'],
        content_type=response_raw.headers['Content-Type'],
        content=response_raw.content
    )

    return response

class LinkFilter:
    def __init__(self, config ):
        self.logger = logging.getLogger(
            'webscraper.LinkFilter')
        self.filters = []
        for filt in config['link_filters']:
            regex = filt['regex']
    
            self.filters.append({
                'regex' : re.compile(regex),
                'occurences' : 0,
                'max_occurences' : filt['max_occurences'],
                'max_depth' : filt['max_depth']
            })

    def filter(self, x, depth):
        for filt in self.filters:
            regex = filt['regex']
            if regex.match(x):
                filt['occurences']=filt['occurences']+1

                if (filt['max_occurences'] == -1) or (filt['occurences']<= filt['max_occurences']):

                    if (filt['max_depth'] != -1) and (depth>=filt['max_depth']):
                        self.logger.debug("Denied (too deep) \"%s\"", x)
                        return False
                    else:
                        self.logger.debug("Link accepted \"%s\"", x)
                        return True
                else:
                    self.logger.debug("Link denied (too much much occurences) \"%s\"", x)
                    return False
        
        self.logger.debug("Link denied (no regex match) \"%s\"", x)
        return False

class RequestToDatabase:
    def __init__(self, cursor, session_id):
        self.session_id = session_id
        self.cursor = cursor

    def response_database_factory(self, request):
        response, _ = webdb.filters.get_response_where_session_id_and_request(
            self.cursor,
            self.session_id,
            request
        )

        module_logger.info("Database request %s completed", request)

        return response


def log_banner():
    module_logger.info("-------------------------------------")
    module_logger.info(" Web scrapper session startet")
    module_logger.info("-------------------------------------")


def init_logger(config):
    logger = logging.getLogger('webscraper')
    logger.setLevel(logging.DEBUG)

    logger2 = logging.getLogger('webdb')
    logger2.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    logdir = config['log_directory']
    if config['logtype'] == "rotate":
        fh = handlers.RotatingFileHandler(
            logdir + config['debug_logfile'], 
            maxBytes=10*1024*1024, 
            backupCount=10
        )
    else:
        fh = logging.FileHandler(
            logdir + config['debug_logfile'], 
            mode='w', 
            encoding="utf-8"
        )

    if (config['loglevel']==1):
        fh.setLevel(logging.DEBUG)
    else:
        fh.setLevel(logging.INFO)

    eh = logging.FileHandler(
        logdir+config['error_logfile'], 
        delay=True, 
        encoding="utf-8"
    )
    eh.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s]: %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    eh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.addHandler(eh)
    logger2.addHandler(fh)
    logger2.addHandler(ch)
    logger2.addHandler(eh)


class WebScraperCommandLineParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="webscraper",
            description='',
            usage=("webscraper <command> [<args]\n"
                   "\n"
                   "The following commands are supported:\n"
                   "   init     Initializes the directories and database file.\n"
                   "   extract  Extract webpage by session id.\n"
                   "   sql      Stores web content into the database.\n"
                   "   slist    Shows a list of stored sessions.\n"
                   "   count    Count the stored content per session.\n"
                   "   info     Shows some useful info of the database.")
        )

        parser.add_argument(
            'command',
            help='Subcommand to run'
        )

        parser.add_argument(
            '--version',
            action='version',
            version='%(prog)s {version}'.format(version=__version__)
        )
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)()

    def init(self):
        parser = argparse.ArgumentParser(
            prog="webscraper init",
            description='Initializes the directories and database file.'
        )

        parser.add_argument('--config', type=str, default=CONFIG_FILE_NAME)

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        
        with open(args.config) as json_data:
            config = json.load(json_data)


        
        logdir = config['log_directory']
        if not os.path.exists(logdir):
            module_logger.info("Created directory %s", logdir)
            os.mkdir(logdir)

        init_logger(config)

        dbdir = config['database_directory']
        if not os.path.exists(dbdir):
            module_logger.info("Created directory %s", dbdir)
            os.mkdir(dbdir)

    def count(self):
        parser = argparse.ArgumentParser(
            prog="webscraper slist",
            description='Stores web content into a database'
        )

        parser.add_argument('--config', type=str, default=CONFIG_FILE_NAME)

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        
        with open(args.config) as json_data:
            config = json.load(json_data)

        init_logger(config)
        connection = webdb.db.open_db_readonly(config['database_directory']+config['database'])
        cursor = connection.cursor()
        content_types = webdb.interface.get_content_types(cursor)
        sessions = webdb.interface.get_sessions(cursor)

        for _, meta in sessions:
            stats = []
            session_id = meta['session_id']
            for content_type in content_types:
                responses_count = len(
                    webdb.filters.get_requests_where_session_id_and_content_type(
                        cursor,
                        session_id,
                        content_type
                    )
                )
                stats.append("\"{}\": {}".format(
                    content_type, responses_count))
            print("{:4} -- {}".format(session_id, ", ".join(stats)))

    def slist(self):
        parser = argparse.ArgumentParser(
            prog="webscraper slist",
            description='Stores web content into a database'
        )

        parser.add_argument('--config', type=str, default=CONFIG_FILE_NAME)

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        
        with open(args.config) as json_data:
            config = json.load(json_data)

        init_logger(config)
        
        connection = webdb.db.open_db_readonly(config['database_directory']+config['database'])
        cursor = connection.cursor()
        sessions = webdb.interface.get_sessions(cursor)

        last_start_datetime = None
        for session, meta in sessions:
            sid = meta['session_id']
            if last_start_datetime:
                delta_last = session.start_datetime - last_start_datetime
            else:
                delta_last = "---"

            last_start_datetime = session.start_datetime
            print("{:4} -- start = {}  end = {}  session_duration = {}  delta = {}".format(
                sid,
                session.start_datetime,
                session.end_datetime,
                session.get_duration(),
                delta_last,
            ))

    def info(self):
        parser = argparse.ArgumentParser(
            prog="webscraper info",
            description='Stores web content into a database'
        )

        parser.add_argument('--config', type=str, default=CONFIG_FILE_NAME)

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        
        with open(args.config) as json_data:
            config = json.load(json_data)

        init_logger(config)
        statinfo = os.stat(config['database'])
        connection = webdb.db.open_db_readonly(config['database_directory']+config['database'])
        cursor = connection.cursor()

        info = webdb.info.info(cursor)
        info_cache = webdb.info.info_cache(cursor)

        content_size = webdb.info.compute_content_size(cursor)

        print(
            "---------------------------------------------------------\n"
            "                            Session count: {}\n"
            "                            Request count: {}\n"
            "                           Response count: {}\n"
            "---------------------------------------------------------\n"
            "                            Content count: {} ({:.2f})\n"
            "                       Content type count: {} ({:.2f})\n"
            "                                URI count: {} ({:.2f})\n"
            "---------------------------------------------------------\n"
            "        Average Request count per session: {:.1f}\n"
            "       Average Response count per session: {:.1f}\n"
            "        Average Content count per session: {:.1f}\n"
            "---------------------------------------------------------\n"
            "                         Size of database: {:.1f} KB\n"
            "              Size of content in database: {:.1f} KB\n"
            "        Size of overhead data in database: {:.1f} KB\n"
            "                           Overhead ratio: {:.2f}\n"
            "                  Average size of session: {:.1f} KB\n"
            "---------------------------------------------------------"
            "".format(
                info['session'],
                info['request'],
                info['response'],
                info_cache['content'][0],
                info_cache['content'][1],
                info_cache['content_type'][0],
                info_cache['content_type'][1],
                info_cache['uri'][0],
                info_cache['uri'][1],
                info['request']/info['session'],
                info['response']/info['session'],
                info_cache['content'][0]/info['session'],
                statinfo.st_size/1024,
                content_size/1024,
                (statinfo.st_size-content_size)/1024,
                (statinfo.st_size-content_size)/statinfo.st_size,
                statinfo.st_size/1024/info['session']
            ))

    def sql(self):
        parser = argparse.ArgumentParser(
            prog="webscraper sql",
            description='Stores web content into a database'
        )

        parser.add_argument('--config', type=str, default=CONFIG_FILE_NAME)

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        
        with open(args.config) as json_data:
            config = json.load(json_data)

        init_logger(config)
        log_banner()

        content_handler_logger = ContentHandlerLogger()
        content_handler_sqlite = ContentHandlerSqlite(config['database_directory']+config['database'])

        content_handler_sqlite.set_component(content_handler_logger)
        link_filter = LinkFilter(config)
        
        webscraper(
            url=config['url'],
            request_to_response=response_factory,
            content_handler=content_handler_sqlite,
            download_img=True,
            link_filter=link_filter.filter
        )

    def extract(self):
        parser = argparse.ArgumentParser(
            prog="webscraper extract",
            description='Extract web content from database'
        )

        # prefixing the argument with -- means it's optional
        parser.add_argument('session_id', type=int)
        parser.add_argument('dirname', type=str)
        parser.add_argument('--config', type=str, default=CONFIG_FILE_NAME)
        
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])

        with open(args.config) as json_data:
            config = json.load(json_data)

        init_logger(config)
        log_banner()

        connection = webdb.db.open_db_readonly(config['database_directory']+config['database'])
        cursor = connection.cursor()
        rtb = RequestToDatabase(cursor, args.session_id)

        content_handler_filesystem = ContentHandlerFilesystem(args.dirname)
        content_handler_logger = ContentHandlerLogger()
        content_handler_filesystem.set_component(content_handler_logger)
        link_filter = LinkFilter(config)

        webscraper(
            url=config['url'],
            request_to_response=rtb.response_database_factory,
            content_handler=content_handler_filesystem,
            download_img=True,
            link_filter=link_filter.filter
        )

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    module_logger.exception("Uncaught exception", exc_info=(
        exc_type, exc_value, exc_traceback))


def main():
        
     # Install exception handler
    sys.excepthook = handle_exception
    WebScraperCommandLineParser()


if __name__ == "__main__":
    main()
