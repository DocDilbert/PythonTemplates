import logging
from content_handler_decorator import ContentHandlerDecorator

class ContentHandlerLogger(ContentHandlerDecorator): 
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('main.content_handler_logger.ContentHandlerLogger')

    def session_started(self):
        super().session_started()
        self.logger.debug("Call: session_started")

    def response_with_html_content_received(self, request, response, response_content):
        super().response_with_html_content_received(request,response, response_content)
        self.logger.debug("Call: response_with_html_content_received\n"
            "\trequest = %s\n"
            "\tresponse = %s\n"
            "\tresponse_content = %s", request, response, response_content)

    def response_with_css_content_received(self, request, response, response_content, tag):
        super().response_with_css_content_received(request, response, response_content, tag)
        self.logger.debug("Call: response_with_css_content_received\n"
            "\trequest = %s\n"
            "\tresponse = %s\n"
            "\tresponse_content = %s", request, response, response_content)

    def response_with_img_content_received(self, request, response, response_content, tag):
        super().response_with_img_content_received(request, response, response_content, tag)
        self.logger.debug("Call: response_with_img_content_received\n"
            "\trequest = %s\n"
            "\tresponse = %s\n"
            "\tresponse_content = %s", request, response, response_content)

    def html_post_process_handler(self, request, soup):
        super().html_post_process_handler(request, soup)
        self.logger.debug("Call: html_post_process_handler\n"
            "\trequest = %s", request)
        
    def session_finished(self):
        super().session_finished()
        self.logger.debug("Call: session_finished")