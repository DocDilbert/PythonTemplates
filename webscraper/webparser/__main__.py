import webdb
import re
import argparse
from bs4 import BeautifulSoup
import time
from lxml import etree
from version import __version__
import sys
import logging
import json
from urllib.parse import urlparse, urlunparse


# create logger
module_logger = logging.getLogger('webparser')

CONTENT_TYPE = "text/html;charset=UTF-8"



class SessionIdUnknown(Exception):
    pass


class FileWriter:
    def __init__(self, mode):
        self.entrylist = []

    def add_entry(self, session_id, features_dict):
        self.entrylist.append(features_dict)

    def write_file(self):
        with open("ss.json","w",encoding="utf-8") as fp:
            json.dump(self.entrylist, fp, indent=4, sort_keys=True)


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

class ResponseParser:
    def __init__(self, add_entry):
        self.regex = re.compile(r"-(\d+)-inline\.")
        self.add_entry = add_entry
    def parse(self, session_id, response):
        soup = BeautifulSoup(response.content.decode("utf-8"), 'lxml')

        results = soup.find_all("div", {"class":"job-element-row"})
        
        for result in results:
            title_tag = result.find(class_='job-element__url-title-text')
            title = title_tag.text.strip("\n")
            
            company_tag = result.find(class_='job-element__body__company')
            company = company_tag.text.strip("\n")

            location_tag = result.find(class_='job-element__body__location')
            location = location_tag.text.strip("\n")

            date_tag = result.find(class_='job-element__date')
            datetime_tag = date_tag.find('time')

            details_tag= result.find(class_='job-element__body__details')
            details = details_tag.text.strip("\n")

            
            url_tag= result.find(class_="job-element__url")
            uuid_search = self.regex.search(url_tag['href'])

            features_dict = {
                'title': title,
                'company': company,
                'location': location,
                'datetime': datetime_tag['datetime'],
                'details' : details,
                'uuid' : uuid_search.group(1),
                'session_id' : session_id
            }
            
            self.add_entry(session_id, features_dict)

def parse_session(cursor, session_id, session, regex, writer):

    print("Parsing session {} / {} --> {}".format(
        session_id,
        session.start_datetime, session.end_datetime
    ))

    requests = webdb.filters.get_requests_where_session_id_and_content_type(
        cursor, session_id, CONTENT_TYPE)

    if regex:
        requests_filtered = (
            request for request, _ in requests
            if regex.match(request.path)
        )
    else:
        requests_filtered = (
            request for request, _ in requests
        )

    responses = (
        webdb.filters.get_response_where_session_id_and_request(
            cursor, session_id, request)
        for request in requests_filtered
    )

    response_parser = ResponseParser(add_entry=writer.add_entry)
    for response, _ in responses:
        response_parser.parse(session_id, response)


def parse_session_list(cursor, session_list, regex, writer):
    for session, meta in session_list:
        session_id = meta['session_id']
        try:
            parse_session(cursor, session_id, session, regex, writer)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            module_logger.exception("Parse session exception", exc_info=(
                exc_type, exc_value, exc_traceback))


def print_exec_time(start, end, max_sessions):
    print()
    print("Execution time {:.3f} s.".format(end - start))
    print("Execution time per session {:.3f} s.".format(
        (end - start)/max_sessions))


def parse_all():
    start = time.time()

    connection = webdb.db.open_db_readonly("webscraper.db")
    cursor = connection.cursor()

    #regex = re.compile("/tankstelle/")
    regex = None
    file_writer = FileWriter("w")
    session_list = webdb.interface.get_sessions(cursor)
    parse_session_list(cursor, session_list, regex, file_writer)
    file_writer.write_file()
    end = time.time()
    max_sessions = session_list[-1][1]['session_id']
    print_exec_time(start, end, max_sessions)


def parse_append():
    start = time.time()
    with open("out.csv", "r") as fp:
        lines = fp.readlines()

    last_session_id = int(lines[-1].split(';')[0])

    connection = webdb.db.open_db_readonly("webscraper.db")
    cursor = connection.cursor()

    session_list = [
        (session, meta) for session, meta in webdb.interface.get_sessions(cursor)
        if meta['session_id'] > last_session_id
    ]

    if len(session_list) == 0:
        print("No new sessions found.")
        return

    regex = re.compile("/tankstelle/")
    
    file_writer = FileWriter("a")
    parse_session_list(cursor, session_list, regex, file_writer)
    end = time.time()

    max_sessions = session_list[-1][1]['session_id']
    print_exec_time(start, end, max_sessions)


def parse_single(session_id):
    start = time.time()
    connection = webdb.db.open_db_readonly("webscraper.db")
    cursor = connection.cursor()

    session_list = [
        (session, meta) for session, meta in webdb.interface.get_sessions(cursor)
        if meta['session_id'] == session_id
    ]

    if len(session_list) != 1:
        raise SessionIdUnknown()

    #regex = re.compile("/tankstelle/")
    regex = None
    file_writer = ConsoleWriter()
    parse_session_list(cursor, session_list, regex, file_writer)
    end = time.time()

    max_sessions = session_list[-1][1]['session_id']
    print_exec_time(start, end, max_sessions)


class WebParserCommandLineParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="webparser",
            description='',
            usage=("webparser <command> [<args]\n"
                   "\n"
                   "The following commands are supported:\n"
                   "   all      parses all sessions stored in the database\n"
                   "   appends  appends new sessions\n"
                   "   single   parses a single session stored in the database\n")
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

    def all(self):
        parse_all()

    def append(self):
        parse_append()

    def single(self):
        parser = argparse.ArgumentParser(
            prog="webparser single",
            description='Parses a single session'
        )

        # prefixing the argument with -- means it's optional
        parser.add_argument('session_id', type=int)
        #parser.add_argument('--outfile', type=str)

        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(sys.argv[2:])
        parse_single(args.session_id)


def init_logger():
    logger = logging.getLogger('webparser')
    logger.setLevel(logging.DEBUG)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    eh = logging.FileHandler('webparser_errors.log', delay=True)
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
