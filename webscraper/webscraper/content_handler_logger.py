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

    def html_content_post_request_handler(self, request, response, tree):
        super().html_content_post_request_handler(request,response, tree)
        
        self.logger.debug("html_content_post_request_handler\n"
            "\trequest = %s\n"
            "\tresponse = %s", request, response)
    
    def html_content_post_process_handler(self, request, tree):
        super().html_content_post_process_handler(request, tree)
        self.logger.debug("Call: html_content_post_process_handler\n"
            "\trequest = %s", request)
        
    def css_content_pre_request_handler(self,  request, tag):
        super().css_content_pre_request_handler(request,  tag)


    def css_content_post_request_handler(self, request, response):
        super().css_content_post_request_handler(request, response)
        self.logger.debug("css_content_post_request_handler\n"
            "\trequest = %s\n"
            "\tresponse = %s", request, response)

    def img_content_pre_request_handler(self, request,tag):
        super().img_content_pre_request_handler(request,  tag)

    def img_content_post_request_handler(self, request, response):
        super().img_content_post_request_handler(request, response)
        
        self.logger.debug("img_content_post_request_handler\n"
            "\trequest = %s\n"
            "\tresponse = %s", request, response)


    def session_finished(self):
        super().session_finished()
        self.logger.debug("Call: session_finished")