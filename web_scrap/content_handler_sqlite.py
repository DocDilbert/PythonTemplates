import logging
from urllib.parse import urlparse,urlunparse
from content_handler_decorator import ContentHandlerDecorator
import sqlliteblob

class ContentHandlerSqlite(ContentHandlerDecorator): 
    def __init__(self):
        super().__init__()
        self.connection =  sqlliteblob.create_or_open_db("requests.db")
        self.logger = logging.getLogger('main.content_handler_sqllite.ContentHandlerSqlite')
    
    def insert_entry(self, scheme, netloc, path, params, query, fragment, response):
        self.logger.debug("insert_entry url_part = { ... \n"+
            "\tscheme = %s\n"+
            "\tnetloc = %s\n"+
            "\tpath = %s\n"+
            "\tparams = %s\n"+
            "\tquery = %s\n"+
            "\tfragment = %s}", scheme, netloc, path, params, query, fragment)
        
        content_type = response.headers['Content-Type']
        
        cursor = self.connection.cursor()
        sqlliteblob.insert_request(cursor,
            scheme, 
            netloc, 
            path, 
            params, 
            query, 
            fragment,
            content_type,
            response.content
        )

        self.connection.commit()
        self.logger.debug("insert_entry response = { ... \n"+
            "\tcontent_type = %s}", content_type)

        

    def response_with_html_content_received(self, url, response):
        super().response_with_html_content_received(url, response)

        parts = urlparse(url)
        self.insert_entry(*parts, response = response)
        
    def response_with_css_content_received(self, url, response, tag):
        super().response_with_css_content_received( url, response, tag)
        parts = urlparse(url)
        self.insert_entry(*parts, response = response)
        
    def response_with_img_content_received(self, url, response, tag):
        super().response_with_img_content_received( url, response, tag)
        parts = urlparse(url)
        self.insert_entry(*parts, response = response)

    def html_post_process_handler(self, url, soup):
        super().html_post_process_handler(url, soup)

