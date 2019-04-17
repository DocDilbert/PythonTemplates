import logging
from content_handler_decorator import ContentHandlerDecorator

class ContentHandlerLogger(ContentHandlerDecorator): 
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger('main.content_handler_logger.ContentHandlerLogger')
    
    def __log_request(self, request):
        self.logger.debug("Log request:\n"
            "\turl = %s",  request['url'])

    def __log_response(self, response):
        self.logger.debug("Log response:\n"
            "\tstatus_code = %i,\n"
            "\theaders = %s,\n"
            "\tcookies = %s,\n"
            "\tencoding = %s", response.status_code, response.headers, response.cookies, response.encoding)

    def response_with_html_content_received(self, request, response):
        super().response_with_html_content_received(request,response)
        self.__log_request(request)
        self.__log_response(response)

    def response_with_css_content_received(self, request, response, tag):
        super().response_with_css_content_received(request, response, tag)
        self.__log_request(request)
        self.__log_response(response)

    def response_with_img_content_received(self, request, response, tag):
        super().response_with_img_content_received(request, response, tag)
        self.__log_request(request)
        self.__log_response(response)

    def html_post_process_handler(self, url, soup):
        super().html_post_process_handler(url, soup)
        self.logger.info("html post process handler was called with url '%s'", url)
        
