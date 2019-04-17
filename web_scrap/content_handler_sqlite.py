import logging
from urllib.parse import urlparse,urlunparse
from content_handler_decorator import ContentHandlerDecorator

class ContentHandlerSqlite(ContentHandlerDecorator): 
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('main.content_handler_sqllite.ContentHandlerSqlite')
    
    def insert_entry(self, scheme, netloc, path, params, query, fragment, response):
        self.logger.debug("insert_entry url_part = { ... \n"+
            " - scheme = %s\n"+
            " - netloc = %s\n"+
            " - path = %s\n"+
            " - params = %s\n"+
            " - query = %s\n"+
            " - fragment = %s\n}", scheme, netloc, path, params, query, fragment)
        
        content_type = response.headers['Content-Type']
        self.logger.debug("insert_entry response = { ... \n"+
            " - content_type = %s\n}", content_type)

        

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

