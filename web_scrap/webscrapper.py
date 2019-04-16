import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse,urlunparse
import os
import time

#chrome 70.0.3538.77
HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}

# create logger
module_logger = logging.getLogger('main.webscraper')

class ExtractFileNameFromURL:
    def __init__(self, url, content_type):
        self.logger = logging.getLogger('main.webscraper.ExtractFileNameFromURL')

        self.logger.debug("url = '%s', content_type = '%s'", url, content_type)
        urlp = urlparse(url)
        self.filename = os.path.basename(urlp.path)
        parts = os.path.splitext(self.filename)
        if parts[1] is '':
            if 'text/html' in content_type:
                self.filename = parts[0]+'.html'
            if 'text/css' in content_type:
                self.filename = parts[0]+'.css'

        self.logger.debug("Isolated parts: %s", parts)
        self.logger.debug("Extracted file name '%s' from url '%s'", self.filename, url)
    
    def __str__(self):
        return self.filename

    def __repr__(self):
        return self.filename

class WebScraperLogger:
    def __init__(self, dirname):
        self.logger = logging.getLogger('main.webscraper.WebScraperLogger')
        self.dirname = dirname
        
        if not os.path.exists(dirname):
            os.mkdir(dirname)
        
    def __log_response_header(self, response):
        self.logger.debug("response header:\n"
            +" - headers = %s, \n - cookies = %s", response.headers, response.cookies)

    def response_with_html_content_received(self, url, response):
        self.logger.info("response with html content received. Source url was '%s'", url)
        self.__log_response_header(response)

        filename = ExtractFileNameFromURL(url, response.headers['Content-type'])

        dest = self.dirname+"/"+str(filename)
        with open(dest,"wb") as file:
            file.write(response.content)

        self.logger.info("Wrote content to '%s'", dest)

    def response_with_css_content_received(self, tag, url, response):
        self.logger.info("response with css content received. Source url was '%s'", url)
        self.__log_response_header(response)

        filename = ExtractFileNameFromURL(url, response.headers['Content-type'])

        dest = self.dirname+"/"+str(filename)
        
        with open(dest,"wb") as file:
            file.write(response.content)
            
        self.logger.info("Wrote content to '%s'", dest)
        tag['href'] = filename


    def response_with_img_content_received(self, tag, url, response):
        self.logger.info("response with img content received. Source url was '%s'", url)
        self.__log_response_header(response)

        filename = ExtractFileNameFromURL(url, response.headers['Content-type'])
        
        dest = self.dirname+"/"+str(filename)
        with open(dest,"wb") as file:
            file.write(response.content)
            
        self.logger.info("Wrote content to '%s'", dest)
        tag['src'] = filename

    def html_process_handler(self, url, soup):
        self.logger.info("html post process handler was called with url '%s'", url)
        
        filename = ExtractFileNameFromURL(url, "text/html; charset=utf-8")

        parts = os.path.splitext(str(filename))
        dest = self.dirname+"/{}_processed{}".format(parts[0], parts[1])
        with open(dest,"wb") as file:
            buf = str(soup.prettify())
            file.write(buf.encode(encoding='UTF-8',errors='strict'))

        self.logger.info("Wrote content to '%s'", dest)


def transform_url(scheme, netloc, url):
    url_parsed = urlparse(url)
    module_logger.debug('transform url url_parse result = %s', url_parsed)

    if not url_parsed.scheme: 
        url_transf = urlunparse((
            scheme,
            netloc,
            url_parsed.path,
            url_parsed.params,
            url_parsed.query,
            url_parsed.fragment))
    else:
        url_transf = url_parsed.geturl()

    module_logger.debug('transform url from %s to %s', url, url_transf)

    return url_transf

def is_internal(netloc, url):
    url_parsed = urlparse(url)

    if url_parsed.netloc == netloc:
        return True
    else:
        return False

def download(scheme, netloc, url, tag, response_handler):
    url_transf = transform_url(scheme, netloc, url)
    module_logger.debug("download - pre request: %s", url_transf)
    img = requests.get(url_transf, headers=HEADERS)
    module_logger.info("Request completed on url %s", url_transf)
    response_handler(tag, url_transf, img)
    

def scrap(url, scraper, download_img=False):
    response = requests.get(url, headers=HEADERS)
    scraper.response_with_html_content_received(url, response)
    soup = BeautifulSoup(response.content, 'html.parser')

    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc

    for link in soup.find_all('link'):
        rel = link.get("rel",None) 
        type_ = link.get("type",None)
        loc = link.get("href")
        module_logger.debug("Found link: %s\n - loc=%s\n - rel=%s\n - type=%s", link, loc, rel, type_)

        # content type css found
        if type_=="text/css" or "stylesheet" in rel:
            download(
                scheme,
                netloc,
                link.get('href'), 
                link, 
                scraper.response_with_css_content_received
            )
            
    if download_img:
        for img in soup.find_all('img', src=True):
            download(
                scheme,
                netloc,
                img.get('src'), 
                img, 
                scraper.response_with_img_content_received
            )
    
    links = []
    for a in soup.find_all('a', href=True):
        link = transform_url(
            scheme, 
            netloc, 
            a.get('href')
        )

        if is_internal(netloc, link):
            links.append(link)

    scraper.html_process_handler(url, soup)
    return links
