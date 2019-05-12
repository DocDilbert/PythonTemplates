import logging
from urllib.parse import urlparse, urlunparse
import datetime

from webtypes.session import Session
from webscraper.content_handler_decorator import ContentHandlerDecorator
import webdb


class ContentHandlerSqlite(ContentHandlerDecorator):
    def __init__(self, filename):
        super().__init__()
        self.connection = webdb.db.create_or_open_db(filename)
        self.cursor = self.connection.cursor()
        self.logger = logging.getLogger(
            'webscraper.content_handler_sqllite.ContentHandlerSqlite')

        self.session_id = -1
        self.session = None

    def session_started(self):
        super().session_started()
        self.session = Session()
        self.session.update_start_datetime()
        self.session_id = webdb.interface.insert_session(self.cursor, self.session)

    def insert_request_and_response(self,  request, response):
        self.logger.debug("Insert request and response into database")

        webdb.interface.insert_request_and_response(
            self.cursor,
            self.session_id,
            request,
            response
        )

    def html_content_post_request_handler(self,  request, response, tree):
        super().html_content_post_request_handler(request, response, tree)
        self.insert_request_and_response(request, response)
    
    def html_content_post_process_handler(self, request, tree):
        super().html_content_post_process_handler(request, tree)

    def css_content_pre_request_handler(self,  request, tag):
        super().css_content_pre_request_handler(request,  tag)

    def css_content_post_request_handler(self,  request, response):
        super().css_content_post_request_handler(request, response)
        self.insert_request_and_response(request, response)

    def img_content_pre_request_handler(self, request,tag):
        super().img_content_pre_request_handler(request,  tag)

    def img_content_post_request_handler(self,  request, response):
        super().img_content_post_request_handler(request, response)
        self.insert_request_and_response(request, response)


    def session_finished(self):
        super().session_finished()

        self.session.update_end_datetime()

        webdb.interface.update_session(
            self.cursor,
            self.session_id,
            self.session
        )

        # erst am Ende committen
        self.connection.commit()
