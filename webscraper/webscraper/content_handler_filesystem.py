import logging
import os
from urllib.parse import urlparse, urlunparse
from webscraper.content_handler_decorator import ContentHandlerDecorator
from lxml import etree

class ExtractFileNameFromURL:
    def __init__(self, url, content_type):
        self.logger = logging.getLogger(
            'webscraper.content_handler_filesystem.ExtractFileNameFromURL')

        self.logger.debug(
            "Arguments: url = '%s', content_type = '%s'", url, content_type)
        urlp = urlparse(url)
        self.filename = os.path.basename(urlp.path)
        parts = os.path.splitext(self.filename)
        self.logger.debug("Splitting of filename results in %s", parts)

        if parts[1] is '':
            if 'text/html' in content_type:
                self.filename = parts[0]+'.html'
            if 'text/css' in content_type:
                self.filename = parts[0]+'.css'

        self.logger.debug(
            "The file name '%s' was extracted from url '%s'", self.filename, url)

    def __str__(self):
        return self.filename

    def __repr__(self):
        return self.filename


class ContentHandlerFilesystem(ContentHandlerDecorator):
    def __init__(self, dirname):
        super().__init__()
        self.logger = logging.getLogger(
            'webscraper.content_handler_filesystem.ContentHandlerFilesystem')
        self.dirname = dirname
        self.html_count = 0

        if not os.path.exists(dirname):
            self.logger.info("Created directory %s", self.dirname)
            os.mkdir(dirname)

    def session_started(self):
        super().session_started()

    def response_with_html_content_received(self, request, response, tree):
        super().response_with_html_content_received(request, response, tree)
        filename = "index_{}.html".format(self.html_count)

        dest = self.dirname+"/"+str(filename)
        html = etree.tostring(
            tree.getroot(), 
            pretty_print=True, 
            method="html"
        )
        
        with open(dest, "wb") as file:
            file.write(
                html
            )

        self.logger.info("Wrote raw html content to '%s'", dest)

    def css_content_pre_request_handler(self,  request, tag):
        super().css_content_pre_request_handler(request,  tag)

    def response_with_css_content_received(self, request, response, tag):
        super().response_with_css_content_received(request, response, tag)
        url = request.get_url()
        filename = ExtractFileNameFromURL(url, response.content_type)

        dest = self.dirname+"/"+str(filename)

        with open(dest, "wb") as file:
            file.write(response.content)

        self.logger.info("Wrote css content to '%s'", dest)
        
        tag.attrib['href'] = str(filename)
    
    def img_content_pre_request_handler(self, request,tag):
        super().img_content_pre_request_handler(request,  tag)

    def response_with_img_content_received(self, request, response, tag):
        super().response_with_img_content_received(request, response, tag)

        url = request.get_url()
        filename = ExtractFileNameFromURL(url, response.content_type)
        dest = self.dirname+"/"+str(filename)

        with open(dest, "wb") as file:
            file.write(response.content)

        self.logger.info("Wrote img content to '%s'", dest)
        tag.attrib['src'] = str(filename)

    def html_post_process_handler(self, request, soup):
        super().html_post_process_handler(request, soup)

        filename = "index_processed_{}.html".format(self.html_count)
        self.html_count += 1
        parts = os.path.splitext(str(filename))
        dest = self.dirname+"/{}_processed{}".format(parts[0], parts[1])
        
        html = etree.tostring(
            soup.getroot(), 
            pretty_print=True, 
            method="html"
        )
        
        with open(dest, "wb") as file:
            file.write(
                html
            )

        self.logger.info("Wrote processed html content to '%s'", dest)
        
    def session_finished(self):
        super().session_finished()
