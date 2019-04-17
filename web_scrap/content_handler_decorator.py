class ContentHandlerDecorator:
    def __init__(self):
        self.component = None

    def set_component(self, component):
        self.component = component

    def response_with_html_content_received(self, url, response):
        if self.component:
            self.component.response_with_html_content_received(url, response)

    def response_with_css_content_received(self,  url, response, tag):
        if self.component:
            self.component.response_with_css_content_received(url, response, tag)

    def response_with_img_content_received(self, url, response, tag):
        if self.component:
            self.component.response_with_img_content_received(url, response, tag)
    
    def html_post_process_handler(self, url, soup):
        if self.component:
            self.component.html_post_process_handler(url, soup)
