import logging
from content_handler_decorator import ContentHandlerDecorator

class ContentHandlerLogger(ContentHandlerDecorator): 
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('main.content_handler_logger.ContentHandlerLogger')
    

    def __response_to_str(self, response):
        return("Log response:\n"
            "\tstatus_code = {},\n"
            "\theaders = {},\n"
            "\tcookies = {},\n"
            "\tencoding = {}".format(response.status_code, response.headers, response.cookies, response.encoding))

    def session_started(self):
        super().session_started()
        self.logger.debug("session_started")

    def response_with_html_content_received(self, request, response, response_content):
        super().response_with_html_content_received(request,response, response_content)
        self.logger.debug("response_with_html_content_received\n"
            "request = %s\n"
            "%s\n"
            "response_content = %s", request, self.__response_to_str(response), response_content)

    def response_with_css_content_received(self, request, response, response_content, tag):
        super().response_with_css_content_received(request, response, response_content, tag)
        self.logger.debug("response_with_css_content_received\n"
            "request = %s\n"
            "%s\n"
            "response_content = %s", request, self.__response_to_str(response), response_content)

    def response_with_img_content_received(self, request, response, response_content, tag):
        super().response_with_img_content_received(request, response, response_content, tag)
        self.logger.debug("response_with_img_content_received\n"
            "request = %s\n"
            "%s\n"
            "response_content = %s", request, self.__response_to_str(response), response_content)

    def html_post_process_handler(self, url, soup):
        super().html_post_process_handler(url, soup)
        self.logger.info("html_post_process_handler\n"
            "url = %s", url)
        
    def session_finished(self):
        super().session_finished()
        self.logger.debug("session_finished")