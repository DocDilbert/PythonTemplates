# -*- coding: utf-8 -*-

import logging
import logging.handlers as handlers
import os
import re
import json
import argparse
import requests
import time
from urllib.parse import urlparse, urlunparse
from cProfile import Profile

import webdb

from webscraper.webscraper import WebScraper
from webscraper.content_handler_sqlite import ContentHandlerSqlite
from webscraper.content_handler_logger import ContentHandlerLogger
from webscraper.content_handler_filesystem import ContentHandlerFilesystem
from webtypes.request import Request
from webtypes.response import Response
import webscraper.request_factories as factories

from version import __version__

# create logger
module_logger = logging.getLogger('webscraper.command_line_parser')


def print_banner():
    print("-------------------------------------")
    print(" Web scrapper session startet")
    print("-------------------------------------")


class CommandLineParser:
    def load_scrapconf(self, name):
        mod = __import__(name, fromlist=[''])
        return mod

    def __init__(self, argv):
        self.argv = argv
        self.logger = logging.getLogger('webscraper.command_line_parser.CommandLineParser')

        parser = argparse.ArgumentParser(
            prog="webscraper",
            description='',
            usage=("webscraper <scrapconf> <command> [<args]\n"
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
            'scrapconf',
            help='Webscraper configuration .py'
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

        args = parser.parse_args(argv[1:3])

        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)
        scrapconf = self.load_scrapconf(args.scrapconf)

        # use dispatch pattern to invoke method with same name
        getattr(self, args.command)(scrapconf)

    def init(self, scrapconf):

        parser = argparse.ArgumentParser(
            prog="webscraper init",
            description='Initializes the directories and database file.'
        )
        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        _args = parser.parse_args(self.argv[3:])

        logdir = scrapconf.LOGDIR
        if not os.path.exists(logdir):
            module_logger.info("Created directory %s", logdir)
            os.mkdir(logdir)

        scrapconf.init_logger()

        dbdir = scrapconf.DATABASE_DIR
        if not os.path.exists(dbdir):
            module_logger.info("Created directory %s", dbdir)
            os.mkdir(dbdir)

    def count(self, scrapconf):
        parser = argparse.ArgumentParser(
            prog="webscraper slist",
            description='Stores web content into a database'
        )

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        _args = parser.parse_args(self.argv[3:])

        scrapconf.init_logger()
        connection = webdb.db.open_db_readonly(
            scrapconf.DATABASE_DIR+scrapconf.DATABASE)
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

    def slist(self, scrapconf):
        parser = argparse.ArgumentParser(
            prog="webscraper slist",
            description='Stores web content into a database'
        )

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        _args = parser.parse_args(self.argv[3:])

        scrapconf.init_logger()

        connection = webdb.db.open_db_readonly(
            scrapconf.DATABASE_DIR+scrapconf.DATABASE)
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

    def info(self, scrapconf):

        parser = argparse.ArgumentParser(
            prog="webscraper info",
            description='Stores web content into a database'
        )

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        _args = parser.parse_args(self.argv[3:])

        scrapconf.init_logger()
        statinfo = os.stat(scrapconf.DATABASE_DIR+scrapconf.DATABASE)
        connection = webdb.db.open_db_readonly(
            scrapconf.DATABASE_DIR+scrapconf.DATABASE)
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

    def sql(self, scrapconf):
        parser = argparse.ArgumentParser(
            prog="webscraper sql",
            description='Stores web content into a database'
        )

        # prefixing the argument with -- means it's optional
        #parser.add_argument('--amend', action='store_true')
        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        parser.add_argument(
            '--profile',
            action='store_true'
        )

       
        args = parser.parse_args(self.argv[3:])

        scrapconf.init_logger()
        print_banner()

        content_handler_logger = ContentHandlerLogger()
        content_handler_sqlite = ContentHandlerSqlite(
            scrapconf.DATABASE_DIR+scrapconf.DATABASE)

        content_handler_sqlite.set_component(content_handler_logger)
        link_filter = scrapconf.LinkFilter()
        request_to_response_factory = factories.RequestToInternet()
        webscraper = WebScraper()

        if args.profile:
            prof = Profile()
            prof.enable()

        webscraper.webscraper(
            url=scrapconf.URL,
            request_to_response_factory=request_to_response_factory,
            content_handler=content_handler_sqlite,
            download_img=True,
            link_filter=link_filter.filter
        )

        if args.profile:
            prof.disable()  # don't profile the generation of stats
            prof.dump_stats('webscraper.prof')

    def extract(self, scrapconf):
        parser = argparse.ArgumentParser(
            prog="webscraper extract",
            description='Extract web content from database'
        )

        # prefixing the argument with -- means it's optional
        parser.add_argument('session_id', type=int)
        parser.add_argument('dirname', type=str)

        # now that we're inside a subcommand, ignore the first
        # TWO argvs, ie the command (git) and the subcommand (commit)
        args = parser.parse_args(self.argv[3:])

        scrapconf.init_logger()
        print_banner()

        request_to_response_factory = factories.RequestToDatabase(
            scrapconf.DATABASE_DIR+scrapconf.DATABASE,
            args.session_id
        )

        content_handler_filesystem = ContentHandlerFilesystem(args.dirname)
        content_handler_logger = ContentHandlerLogger()
        content_handler_filesystem.set_component(content_handler_logger)
        link_filter = scrapconf.LinkFilter()

        webscraper = WebScraper()

        webscraper.webscraper(
            url=scrapconf.URL,
            request_to_response_factory=request_to_response_factory,
            content_handler=content_handler_filesystem,
            download_img=True,
            link_filter=link_filter.filter
        )

