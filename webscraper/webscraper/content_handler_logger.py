import logging
from webscraper.content_handler_decorator import ContentHandlerDecorator
from  datetime import datetime, timedelta
class ContentHandlerLogger(ContentHandlerDecorator): 
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('webscraper.content_handler_logger.ContentHandlerLogger')
    

    def session_started(self):
        super().session_started()
        self.logger.debug("Call: session_started")

    def response_with_html_content_received(self, request, response):
        super().response_with_html_content_received(request,response)
        
        self.logger.debug("response_with_html_content_received\n"
            "\trequest = %s\n"
            "\tresponse = %s", request, response)

    def response_with_css_content_received(self, request, response, tag):
        super().response_with_css_content_received(request, response, tag)
        self.logger.debug("response_with_css_content_received\n"
            "\trequest = %s\n"
            "\tresponse = %s", request, response)

    def response_with_img_content_received(self, request, response, tag):
        super().response_with_img_content_received(request, response, tag)
        
        self.logger.debug("response_with_img_content_received\n"
            "\trequest = %s\n"
            "\tresponse = %s", request, response)

    def html_post_process_handler(self, request, soup):
        super().html_post_process_handler(request, soup)
        self.logger.debug("Call: html_post_process_handler\n"
            "\trequest = %s", request)
        
    def session_finished(self):
        super().session_finished()
        self.logger.debug("Call: session_finished")