import logging
from urllib.parse import urlparse,urlunparse
from content_handler_decorator import ContentHandlerDecorator
import sqlliteblob

class ContentHandlerSqlite(ContentHandlerDecorator): 
    def __init__(self):
        super().__init__()
        self.connection =  sqlliteblob.create_or_open_db("requests.db")
        self.logger = logging.getLogger('main.content_handler_sqllite.ContentHandlerSqlite')
    
    def insert_entry(self, url, response):        
        content_type = response.headers['Content-Type']
        
        self.logger.debug("Try to insert request into database\n"
            "\turl =%s\n" 
            "\tcontent_type = %s", url, content_type)

        cursor = self.connection.cursor()

        sqlliteblob.insert_request(cursor,
            url,
            content_type,
            response.content
        )

        self.connection.commit()
        
    def response_with_html_content_received(self, url, response):
        super().response_with_html_content_received(url, response)
        self.insert_entry(url, response = response)
        
    def response_with_css_content_received(self, url, response, tag):
        super().response_with_css_content_received( url, response, tag)
        self.insert_entry(url, response = response)
        
    def response_with_img_content_received(self, url, response, tag):
        super().response_with_img_content_received( url, response, tag)
        self.insert_entry(url, response = response)

    def html_post_process_handler(self, url, soup):
        super().html_post_process_handler(url, soup)

