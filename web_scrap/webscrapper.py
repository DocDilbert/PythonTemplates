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

        self.logger.debug("parts: %s", parts)
        self.logger.info("Extracted file name '%s' from url '%s'", self.filename, url)
    
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

    def html_download_handler(self, url, page):
        self.logger.info("html download handler was called with url '%s'", url)
        self.logger.debug("html download handler:\n"
            +" - headers = %s, \n - cookies = %s", page.headers, page.cookies)

        filename = ExtractFileNameFromURL(url, page.headers['Content-type'])

        dest = self.dirname+"/"+str(filename)
        with open(dest,"wb") as file:
            file.write(page.content)

        self.logger.info("Wrote content to '%s'", dest)

    def css_downloaded_handler(self, tag, url, link_get):
        self.logger.info("css downloaded handler was called with url '%s'", url)
        self.logger.debug("css downloaded handler:\n"
            +" - tag = %s,\n - headers = %s, \n - cookies = %s", tag, link_get.headers, link_get.cookies)
      
        filename = ExtractFileNameFromURL(url, link_get.headers['Content-type'])
        
        dest = self.dirname+"/"+str(filename)
        with open(dest,"wb") as file:
            file.write(link_get.content)
            
        self.logger.info("Wrote content to '%s'", dest)
        tag['href'] = filename


    def img_downloaded_handler(self, tag, url, link_get):
        self.logger.info("img downloaded handler was called with url '%s'", url)
        self.logger.debug("img downloaded handler:\n"
            +" - tag = %s,\n - headers = %s, \n - cookies = %s", tag, link_get.headers, link_get.cookies)
      
        filename = ExtractFileNameFromURL(url, link_get.headers['Content-type'])
        
        dest = self.dirname+"/"+str(filename)
        with open(dest,"wb") as file:
            file.write(link_get.content)
            
        self.logger.info("Wrote content to '%s'", dest)
        tag['src'] = filename

    def html_post_process_handler(self, url, soup):
        self.logger.info("html post process handler was called with url '%s'", url)
        
        filename = ExtractFileNameFromURL(url, "text/html; charset=utf-8")

        parts = os.path.splitext(str(filename))
        dest = self.dirname+"/{}_processed{}".format(parts[0], parts[1])
        with open(dest,"w") as file:
            file.write(soup.prettify())

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

def download(scheme, netloc, url, tag, handler):
    url_transf = transform_url(scheme, netloc, url)
    module_logger.info("pre request: %s", url_transf)
    img = requests.get(url_transf, headers=HEADERS)
    module_logger.info("post request: %s", url_transf)
    handler(tag, url_transf, img)
    

def scrap(url, scraper):
    response = requests.get(url, headers=HEADERS)
    scraper.html_download_handler(url, response)
    soup = BeautifulSoup(response.content, 'html.parser')

    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc

    for link in soup.find_all('link', {"type" : "text/css"}):
        download(
            scheme,
            netloc,
            link.get('href'), 
            link, 
            scraper.css_downloaded_handler
        )

    for img in soup.find_all('img', src=True):
        download(
            scheme,
            netloc,
            img.get('src'), 
            img, 
            scraper.img_downloaded_handler
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

    scraper.html_post_process_handler(url, soup)
    return links
