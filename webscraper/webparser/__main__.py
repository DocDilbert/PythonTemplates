import webdb
import re
import argparse

import time
from lxml import etree
from version import __version__
import sys
import logging
import json
from urllib.parse import urlparse, urlunparse
import os
import pprint

# create logger
module_logger = logging.getLogger('webparser')

class SessionIdUnknown(Exception):
    pass

class FileWriter:
    def __init__(self, filename):
        self.session_dict = {}
        self.filename = filename


    def add_entry(self, session_id, features_dict):
        sid = int(session_id)
        if sid not in self.session_dict:
            self.session_dict[sid] = []
        self.session_dict[sid].append(features_dict)

    def write_file(self):
        with open(self.filename, "w", encoding="utf-8") as fp:
            json.dump(self.session_dict, fp, indent=4, sort_keys=True)


class DummyWriter:
    def __init__(self):
        pass

    def add_entry(self, session_id, features_dict):
        pass


class ConsoleWriter:
    def __init__(self):
        pass

    def add_entry(self, session_id, features_dict):
        print(features_dict)

def parse_session(parseconf, cursor, session_id, session, writer):

    print("Parsing session {} / {} --> {}".format(
        session_id,
        session.start_datetime, session.end_datetime
    ))

    content_types = webdb.interface.get_content_types(cursor)
    html_type = next((x for x in content_types if "text/html" in x))

    requests = webdb.filters.get_requests_where_session_id_and_content_type(
        cursor, session_id, html_type)

    transfers = (
        (
            request[0],
            webdb.filters.get_response_where_session_id_and_request(cursor, session_id, request[0])[0]
        )
        for request in requests
    )

    response_parser = parseconf.ResponseParser(add_entry=writer.add_entry)
    for request, response in transfers:
        response_parser.parse(session_id, request, response)


def parse_session_list(parseconf,  cursor, session_list, writer):
    for session, meta in session_list:
        session_id = meta['session_id']
        try:
            parse_session(parseconf, cursor, session_id, session, writer)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            module_logger.exception("Parse session exception", exc_info=(
                exc_type, exc_value, exc_traceback))


def print_exec_time(start, end, max_sessions):
    print()
    print("Execution time {:.3f} s.".format(end - start))
    print("Execution time per session {:.3f} s.".format(
        (end - start)/max_sessions))


def parse_all(parseconf):
    start = time.time()

    connection = webdb.db.open_db_readonly(parseconf.DATABASE_DIR + parseconf.DATABASE)
    cursor = connection.cursor()

    file_writer = FileWriter(filename = parseconf.RAW_DATA_DIR + parseconf.RAW_DATA_FILE)
    session_list = webdb.interface.get_sessions(cursor)
    parse_session_list(parseconf, cursor, session_list, file_writer)

    file_writer.write_file()
    end = time.time()
    max_sessions = session_list[-1][1]['session_id']
    print_exec_time(start, end, max_sessions)

def parse_single(parseconf, session_id):
    start = time.time()
    connection = webdb.db.open_db_readonly(parseconf.DATABASE_DIR + parseconf.DATABASE)
    cursor = connection.cursor()

    session_list = [
        (session, meta) for session, meta in webdb.interface.get_sessions(cursor)
        if meta['session_id'] == session_id
    ]

    if len(session_list) != 1:
        raise SessionIdUnknown()


    file_writer = ConsoleWriter()
    parse_session_list(parseconf, cursor, session_list, file_writer)
    end = time.time()

    max_sessions = session_list[-1][1]['session_id']
    print_exec_time(start, end, max_sessions)


class WebParserCommandLineParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="webparser",
            description='',
            usage=("webparser <parseconf> <command> [<args]\n"
                   "\n"
                   "The following commands are supported:\n"
                   "   all      parses all sessions stored in the database\n"
                   "   single   parses a single session stored in the database\n")
        )
        
        parser.add_argument(
            'parseconf',
            help='Parser configuration .py'
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
        args = parser.parse_args(sys.argv[1:3])

        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        parseconf = self.load_parseconf(args.parseconf)
        dirname = parseconf.RAW_DATA_DIR
        if not os.path.exists(dirname):
            module_logger.info("Created directory %s", dirname)
            os.mkdir(dirname)
        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)(parseconf)

    def load_parseconf(self, name):
        mod = __import__(name, fromlist=[''])
        return mod


    def all(self, parseconf):
        parser = argparse.ArgumentParser(
            prog="webparser all",
            description='Parsesall sessions'
        )
        _args = parser.parse_args(sys.argv[3:])
        parse_all(parseconf)

    def single(self, parseconf):
        parser = argparse.ArgumentParser(
            prog="webparser single",
            description='Parses a single session'
        )

        # prefixing the argument with -- means it's optional
        parser.add_argument('session_id', type=int)
        #parser.add_argument('--outfile', type=str)

        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[3:])
        parse_single(parseconf, args.session_id)


def init_logger():
    logger = logging.getLogger('webparser')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    eh = logging.FileHandler('log/webparser_errors.log', delay=True)
    eh.setLevel(logging.ERROR)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s]: %(message)s')

    ch.setFormatter(formatter)
    eh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(eh)


def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    module_logger.exception("Uncaught exception", exc_info=(
        exc_type, exc_value, exc_traceback))


def main():

   

    init_logger()

    # Install exception handler

    sys.excepthook = handle_exception
    WebParserCommandLineParser()


if __name__ == "__main__":
    main()
