import logging
from urllib.parse import urlparse,urlunparse
from content_handler_decorator import ContentHandlerDecorator
import sqlliteblob
import datetime

class ContentHandlerSqlite(ContentHandlerDecorator): 
    def __init__(self):
        super().__init__()
        self.connection =  sqlliteblob.create_or_open_db("requests.db")
        self.logger = logging.getLogger('main.content_handler_sqllite.ContentHandlerSqlite')
        self.timestamp = datetime.datetime.now().isoformat()

    def insert_request_and_response(self,  request, response):        
        self.logger.debug("Insert request and response into database")

        cursor = self.connection.cursor()
        content_type = response.headers['Content-Type']
        sqlliteblob.insert_request_and_response(cursor,
            self.timestamp,
            request,
            content_type,
            response.content
        )
    def session_started(self):
        super().session_started()

    def response_with_html_content_received(self,  request, response):
        super().response_with_html_content_received( request, response)
        self.insert_request_and_response(request, response)
        
    def response_with_css_content_received(self,  request, response, tag):
        super().response_with_css_content_received(  request, response, tag)
        self.insert_request_and_response(request, response)
        
    def response_with_img_content_received(self,  request, response, tag):
        super().response_with_img_content_received(  request, response, tag)
        self.insert_request_and_response( request, response)

    def html_post_process_handler(self, url, soup):
        super().html_post_process_handler(url, soup)

    def session_finished(self):
        super().session_finished()
        
        # erst am Ende committen
        self.connection.commit() 
