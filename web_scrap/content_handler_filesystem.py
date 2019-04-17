import logging
import os
from urllib.parse import urlparse,urlunparse
from content_handler_decorator import ContentHandlerDecorator

class ExtractFileNameFromURL:
    def __init__(self, url, content_type):
        self.logger = logging.getLogger('main.content_handler_filesystem.ExtractFileNameFromURL')

        self.logger.debug("Arguments: url = '%s', content_type = '%s'", url, content_type)
        urlp = urlparse(url)
        self.filename = os.path.basename(urlp.path)
        parts = os.path.splitext(self.filename)
        self.logger.debug("Splitting of filename results in %s", parts)

        if parts[1] is '':
            if 'text/html' in content_type:
                self.filename = parts[0]+'.html'
            if 'text/css' in content_type:
                self.filename = parts[0]+'.css'
        
        self.logger.debug("The file name '%s' was extracted from url '%s'", self.filename, url)
    
    def __str__(self):
        return self.filename

    def __repr__(self):
        return self.filename

class ContentHandlerFilesystem(ContentHandlerDecorator): 
    def __init__(self, dirname):
        super().__init__()
        self.logger = logging.getLogger('main.content_handler_filesystem.ContentHandlerFilesystem')
        self.dirname = dirname
        
        if not os.path.exists(dirname):
            self.logger.info("Created directory %s", self.dirname )
            os.mkdir(dirname)
    
    def response_with_html_content_received(self, url, response):
        super().response_with_html_content_received(url, response)

        filename = ExtractFileNameFromURL(url, response.headers['Content-type'])

        dest = self.dirname+"/"+str(filename)
        with open(dest,"wb") as file:
            file.write(response.content)

        self.logger.info("Wrote raw html content to '%s'", dest)

    def response_with_css_content_received(self, url, response, tag):
        super().response_with_css_content_received( url, response, tag)

        filename = ExtractFileNameFromURL(url, response.headers['Content-type'])

        dest = self.dirname+"/"+str(filename)
        
        with open(dest,"wb") as file:
            file.write(response.content)
            
        self.logger.info("Wrote css content to '%s'", dest)
        tag['href'] = filename


    def response_with_img_content_received(self, url, response, tag):
        super().response_with_img_content_received( url, response, tag)

        filename = ExtractFileNameFromURL(url, response.headers['Content-type'])
        
        dest = self.dirname+"/"+str(filename)
        with open(dest,"wb") as file:
            file.write(response.content)
            
        self.logger.info("Wrote img content to '%s'", dest)
        tag['src'] = filename

    def html_post_process_handler(self, url, soup):
        super().html_post_process_handler(url, soup)

        filename = ExtractFileNameFromURL(url, "text/html; charset=utf-8")

        parts = os.path.splitext(str(filename))
        dest = self.dirname+"/{}_processed{}".format(parts[0], parts[1])
        with open(dest,"wb") as file:
            buf = str(soup.prettify())
            file.write(buf.encode(encoding='UTF-8', errors='strict'))

        self.logger.info("Wrote processed html content to '%s'", dest)
