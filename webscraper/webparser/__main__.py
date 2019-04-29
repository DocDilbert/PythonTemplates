import webdb
import re
import argparse
from bs4 import BeautifulSoup
import time
from lxml import etree
from version import __version__
import sys
import logging


# create logger
module_logger = logging.getLogger('webparser')

CONTENT_TYPE="text/html; charset=UTF-8"

class FileWriter:
    def __init__(self, mode):
        self.f = open("out.csv", mode,  encoding="utf-8")

    def add_entry(self, session_id, uuid, headline, adress, products ):
        
        for zahl, product,wann1, wann2 in products:
            self.f.write('{};"{}";"{}";"{}";"{}";"{}";"{}";"{}"\n'.format(
                session_id,
                uuid, 
                headline, 
                "#?#".join(adress),
                zahl, 
                product,
                wann1,
                wann2
            ))

class DummyWriter:
    def __init__(self):
        pass

    def add_entry(self, session_id, uuid, headline, adress, products ):
        pass

def parse_response(session_id, response, add_entry):
    p3 = time.time()
    soup = BeautifulSoup(response.content.decode("utf-8") ,'lxml')
    p3 = time.time() - p3

    p4 =  time.time()
    div_with_data = soup.find("div", {"data-tankstelle": True})
    uuid = div_with_data["data-tankstelle"]

    headline_tag = div_with_data.find("h4", {"class" : "headline"})
    headline = headline_tag.string

    address_tag = headline_tag.find_next("p").find_next("p")

    #Extract adress
    adress = address_tag.text.split("\n")
    adress = adress[2:]
    adress[0] = adress[0].replace("\r","")
   
    products = []
    div_with_class_preis = address_tag.find_all_next("div", {"class","preis"})
    
    for preisc in div_with_class_preis:

        span_with_class_zahl = preisc.find("span", {"class","zahl"}).text
        
        product = preisc.find("strong").text
        
        span_with_title=preisc.find("span", {"title":True})
        if not span_with_title:
            continue
        wann1 = str.strip(str(span_with_title.next_sibling))
        wann2 = span_with_title['title']
        
        products.append([
            span_with_class_zahl, 
            product,
            wann1,
            wann2
        ])
        
    add_entry(session_id, uuid, headline, adress, products)
    p4 = time.time() - p4
    return p3, p4

def parse_session(cursor, session_id, session, regex, file_writer):

    print("Parsing session {} / {} --> {}".format(session_id, session.start_datetime, session.end_datetime))
        
    p1_start = time.time()
    requests = webdb.filters.get_requests_where_session_id_and_content_type(cursor, session_id, CONTENT_TYPE)

    requests_filtered = [request for request,_ in requests if regex.match(request.path)]
    
    responses = [
        webdb.filters.get_response_where_session_id_and_request(cursor, session_id, request) 
        for request in requests_filtered
    ]
    p1 = time.time() - p1_start
    
    p2_start = time.time()
    p2_0 = 0
    p2_1 = 0
    for response,_ in responses:
        p2_0_, p2_1_ = parse_response(session_id, response, add_entry=file_writer.add_entry)
        p2_0 = p2_0 + p2_0_
        p2_1 = p2_1 + p2_1_

    p2 = time.time() - p2_start

    return p1, p2, p2_0, p2_1
def parse():
    
    start = time.time()

    connection = webdb.db.open_db_readonly("webscraper.db")
    cursor = connection.cursor()

    regex = re.compile("/tankstelle/")

    p1 = 0
    p2 = 0
    p2_0 = 0
    p2_1 = 0

    file_writer = FileWriter("w")
    for session, meta in webdb.interface.get_sessions(cursor):
        session_id = meta['session_id']
        p1_, p2_, p2_0_, p2_1_ = parse_session(cursor, session_id, session, regex, file_writer)
        p1 += p1_
        p2 += p2_
        p2_0 += p2_0_
        p2_1 += p2_1_
        
    end = time.time()
    max_sessions = session_id
    
    print()
    print("Execution time {:.3f} s.".format(end - start))
    print("Execution time per session {:.3f} s.".format((end - start)/max_sessions))
    print("----")
    print("  avg(p1) = {:.3f} s (database access time)".format(p1/max_sessions))
    print("  avg(p2) = {:.3f} s (parsing time)".format(p2/max_sessions))
    print("----")
    print("avg(p2_0) = {:.3f} s (creation time)".format(p2_0/max_sessions))
    print("avg(p2_1) = {:.3f} s (searching time)".format(p2_1/max_sessions))
    print("----")

def parse_append():
    with open("out.csv", "r") as fp:
        lines = fp.readlines()

    last_session_id = int(lines[-1].split(';')[0])

    connection = webdb.db.open_db_readonly("webscraper.db")
    cursor = connection.cursor()

    sessions = (
        (session, meta) for session, meta in webdb.interface.get_sessions(cursor) 
        if meta['session_id']>last_session_id
    )

    for session, meta in sessions:
        print(meta)

class WebParserCommandLineParser:
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="webparser",
            description='',
            usage=("webscraper <command> [<args]\n"
                   "\n"
                   "The following commands are supported:\n"
                   "   parse    parses the database")
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

    def parse(self):
        parse()
    
    def append(self):
        parse_append()

    
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    module_logger.exception("Uncaught exception", exc_info=(
        exc_type, exc_value, exc_traceback))


def main():

     # Install exception handler
    sys.excepthook = handle_exception
    WebParserCommandLineParser()


if __name__ == "__main__":
    main()