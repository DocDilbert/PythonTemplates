import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse,urlunparse
import os
import time

#chrome 70.0.3538.77
HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

# create logger
module_logger = logging.getLogger('main.webscraper')


def transform_url(scheme, netloc, url):
    url_parsed = urlparse(url)
    module_logger.debug('Transform url with url_parse results in = %s', url_parsed)

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

    module_logger.debug('Transform url from %s to %s', url, url_transf)

    return url_transf

def is_internal(netloc, url):
    url_parsed = urlparse(url)

    if url_parsed.netloc == netloc:
        return True
    else:
        return False

def download(scheme, netloc, url, tag, response_handler):
    url_transf = transform_url(scheme, netloc, url)
    module_logger.debug("Performing Request on url %s", url_transf)
    img = requests.get(url_transf, headers=HEADERS)
    module_logger.info("Request completed on url %s", url_transf)
    response_handler(url_transf, img, tag)
    
def scrap(url, content_handler, download_img=False):
    response = requests.get(url, headers=HEADERS)
    module_logger.info("Request completed on url %s", url)
    content_handler.response_with_html_content_received(url, response)

    soup = BeautifulSoup(response.content, 'html.parser')

    parsed_url = urlparse(url)
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc

    for link in soup.find_all('link'):
        rel = link.get("rel", None) 
        type_ = link.get("type", None)
        loc = link.get("href")
        module_logger.debug("Found link: %s\n"
            "\tloc=%s\n"
            "\trel=%s\n"
            "\ttype=%s", link, loc, rel, type_)

        # content type css found
        if type_=="text/css" or "stylesheet" in rel:
            download(
                scheme,
                netloc,
                link.get('href'), 
                link, 
                content_handler.response_with_css_content_received
            )
            
    if download_img:
        for img in soup.find_all('img', src=True):
            download(
                scheme,
                netloc,
                img.get('src'), 
                img, 
                content_handler.response_with_img_content_received
            )
    
    links = []
    for a in soup.find_all('a', href=True):
        module_logger.debug("Found a with href: %s", a)
        link = transform_url(
            scheme, 
            netloc, 
            a.get('href')
        )

        if is_internal(netloc, link):
            links.append(link)

    content_handler.html_post_process_handler(url, soup)
    return links
