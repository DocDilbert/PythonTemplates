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

    def response_with_html_content_received(self, request, response, tree):
        super().response_with_html_content_received(request,response, tree)
        
        self.logger.debug("response_with_html_content_received\n"
            "\trequest = %s\n"
            "\tresponse = %s", request, response)

    def css_content_pre_request_handler(self,  request, tag):
        super().css_content_pre_request_handler(request,  tag)


    def css_content_post_request_handler(self, request, response, tag):
        super().css_content_post_request_handler(request, response, tag)
        self.logger.debug("css_content_post_request_handler\n"
            "\trequest = %s\n"
            "\tresponse = %s", request, response)

    def img_content_pre_request_handler(self, request,tag):
        super().img_content_pre_request_handler(request,  tag)

    def img_content_post_request_handler(self, request, response, tag):
        super().img_content_post_request_handler(request, response, tag)
        
        self.logger.debug("img_content_post_request_handler\n"
            "\trequest = %s\n"
            "\tresponse = %s", request, response)

    def html_post_process_handler(self, request, soup):
        super().html_post_process_handler(request, soup)
        self.logger.debug("Call: html_post_process_handler\n"
            "\trequest = %s", request)
        
    def session_finished(self):
        super().session_finished()
        self.logger.debug("Call: session_finished")