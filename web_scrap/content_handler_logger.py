import logging
from content_handler_decorator import ContentHandlerDecorator

class ContentHandlerLogger(ContentHandlerDecorator): 
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('main.content_handler_logger.ContentHandlerLogger')
    
    def __log_response(self, response):
        self.logger.debug("Received response:\n"
            +" - status_code = %i,\n"
            +" - headers = %s,\n"
            +" - cookies = %s,\n"
            +" - encoding = %s", response.status_code, response.headers, response.cookies,response.encoding)

    def response_with_html_content_received(self, url, response):
        super().response_with_html_content_received(url,response)

        self.logger.info("Response with html content received. Source url was '%s'", url)
        self.__log_response(response)

    def response_with_css_content_received(self, url, response, tag):
        super().response_with_css_content_received(url, response, tag)
        self.logger.info("Response with css content received. Source url was '%s'", url)
        self.__log_response(response)

    def response_with_img_content_received(self, url, response, tag):
        super().response_with_img_content_received(url, response, tag)
        self.logger.info("Response with img content received. Source url was '%s'", url)
        self.__log_response(response)

    def html_post_process_handler(self, url, soup):
        super().html_post_process_handler(url, soup)
        self.logger.info("html post process handler was called with url '%s'", url)
        
