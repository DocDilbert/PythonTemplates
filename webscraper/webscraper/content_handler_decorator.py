class ContentHandlerDecorator:
    def __init__(self):
        self.component = None

    def set_component(self, component):
        self.component = component

    def session_started(self):
        if self.component:
            self.component.session_started()

    def response_with_html_content_received(self, request, response):
        if self.component:
            self.component.response_with_html_content_received(request, response)

    def response_with_css_content_received(self,  request, response, tag):
        if self.component:
            self.component.response_with_css_content_received(request, response, tag)

    def response_with_img_content_received(self, request, response, tag):
        if self.component:
            self.component.response_with_img_content_received(request, response, tag)
    
    def html_post_process_handler(self, request, soup):
        if self.component:
            self.component.html_post_process_handler(request, soup)

    def session_finished(self):
        if self.component:
            self.component.session_finished()