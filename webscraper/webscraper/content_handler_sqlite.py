import logging
from urllib.parse import urlparse, urlunparse
import datetime

from webtypes.session import Session
from webscraper.content_handler_decorator import ContentHandlerDecorator
import sqliteblob.sqliteblob as sqliteblob


class ContentHandlerSqlite(ContentHandlerDecorator):
    def __init__(self, filename):
        super().__init__()
        self.connection = sqliteblob.create_or_open_db(filename)
        self.cursor = self.connection.cursor()
        self.logger = logging.getLogger(
            'webscraper.content_handler_sqllite.ContentHandlerSqlite')

        self.session_id = -1
        self.session = None

    def session_started(self):
        super().session_started()
        self.session = Session()
        self.session.update_start_datetime()
        self.session_id = sqliteblob.insert_session(self.cursor, self.session)

    def insert_request_and_response(self,  request, response, response_contents):
        self.logger.debug("Insert request and response into database")

        sqliteblob.insert_request_and_response(
            self.cursor,
            self.session_id,
            request,
            response,
            response_contents
        )

    def response_with_html_content_received(self,  request, response, response_content):
        super().response_with_html_content_received(request, response, response_content)
        self.insert_request_and_response(request, response, response_content)

    def response_with_css_content_received(self,  request, response, response_content, tag):
        super().response_with_css_content_received(
            request, response, response_content, tag)
        self.insert_request_and_response(request, response, response_content)

    def response_with_img_content_received(self,  request, response, response_content, tag):
        super().response_with_img_content_received(
            request, response, response_content, tag)
        self.insert_request_and_response(request, response, response_content)

    def html_post_process_handler(self, request, soup):
        super().html_post_process_handler(request, soup)

    def session_finished(self):
        super().session_finished()

        self.session.update_end_datetime()

        sqliteblob.update_session(
            self.cursor,
            self.session_id,
            self.session
        )

        # erst am Ende committen
        self.connection.commit()
