class ContentHandlerDecorator:
    def __init__(self):
        self.component = None

    def set_component(self, component):
        self.component = component

    def session_started(self):
        if self.component:
            self.component.session_started()

    def response_with_html_content_received(self, request, response, tree):
        if self.component:
            self.component.response_with_html_content_received(request, response, tree)

    def css_content_pre_request_handler(self,  request, tag):
        if self.component:
            self.component.css_content_pre_request_handler(request,  tag)

    def css_content_post_request_handler(self,  request, response, tag):
        if self.component:
            self.component.css_content_post_request_handler(request, response, tag)

    def img_content_pre_request_handler(self, request,tag):
        if self.component:
            self.component.img_content_pre_request_handler(request,  tag)

    def img_content_post_request_handler(self, request, response, tag):
        if self.component:
            self.component.img_content_post_request_handler(request, response, tag)
    
    def html_post_process_handler(self, request, soup):
        if self.component:
            self.component.html_post_process_handler(request, soup)

    def session_finished(self):
        if self.component:
            self.component.session_finished()