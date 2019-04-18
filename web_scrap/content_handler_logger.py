import logging
from content_handler_decorator import ContentHandlerDecorator

class ContentHandlerLogger(ContentHandlerDecorator): 
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('main.content_handler_logger.ContentHandlerLogger')
    
    def __request_to_str(self, request):
        return("Log request:\n"
            "\turl = {}".format(request['url']))

    def __response_to_str(self, response):
        return("Log response:\n"
            "\tstatus_code = {},\n"
            "\theaders = {},\n"
            "\tcookies = {},\n"
            "\tencoding = {}".format(response.status_code, response.headers, response.cookies, response.encoding))

    def session_started(self):
        super().session_started()
        self.logger.debug("session_started")

    def response_with_html_content_received(self, request, response):
        super().response_with_html_content_received(request,response)
        self.logger.debug("response_with_html_content_received\n"
            "%s\n"
            "%s", self.__request_to_str(request), self.__response_to_str(response))

    def response_with_css_content_received(self, request, response, tag):
        super().response_with_css_content_received(request, response, tag)
        self.logger.debug("response_with_css_content_received\n"
            "%s\n"
            "%s", self.__request_to_str(request), self.__response_to_str(response))

    def response_with_img_content_received(self, request, response, tag):
        super().response_with_img_content_received(request, response, tag)
        self.logger.debug("response_with_img_content_received\n"
            "%s\n"
            "%s", self.__request_to_str(request), self.__response_to_str(response))

    def html_post_process_handler(self, url, soup):
        super().html_post_process_handler(url, soup)
        self.logger.info("html_post_process_handler\n"
            "url = %s", url)
        
    def session_finished(self):
        super().session_finished()
        self.logger.debug("session_finished")