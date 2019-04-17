import logging
from content_handler_decorator import ContentHandlerDecorator

class ContentHandlerSqlite(ContentHandlerDecorator): 
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('main.content_handler_sqllite.ContentHandlerSqlite')
    
    def response_with_html_content_received(self, url, response):
        super().response_with_html_content_received(url, response)
        self.logger.info("response_with_html_content_received")

    def response_with_css_content_received(self, url, response, tag):
        super().response_with_css_content_received( url, response, tag)
        self.logger.info("response_with_css_content_received")
        
    def response_with_img_content_received(self, url, response, tag):
        super().response_with_img_content_received( url, response, tag)
        self.logger.info("response_with_img_content_received")

    def html_post_process_handler(self, url, soup):
        super().html_post_process_handler(url, soup)
        self.logger.info("html_post_process_handler")

