import requests
import logging
import os
import time
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse


from webtypes.request import Request
from webtypes.response import Response
from webtypes.response_content import ResponseContent

#chrome 70.0.3538.77
HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

# create logger
module_logger = logging.getLogger('webscraper.webscraper')


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
            url_parsed.fragment)
        )
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


def download(request_to_response, scheme, netloc, url, tag, response_handler):
    url_transf = transform_url(scheme, netloc, url)
    module_logger.debug("Performing Request on url %s", url_transf)

    request = Request.from_url(url_transf)
    response, RESPONSE_CONTENTS = request_to_response(request) 
    response_handler(request, response, RESPONSE_CONTENTS, tag)

def scrap(
    request, 
    request_to_response, 
    content_handler, 
    download_img=False,
    link_filter=None,
    max_level=1,
    level=0,
):
    if level==max_level:
        module_logger.info("Maximal recursion level reached.")
        return

    response, RESPONSE_CONTENTS = request_to_response(request) 
    content_handler.response_with_html_content_received(request, response, RESPONSE_CONTENTS)

    soup = BeautifulSoup(RESPONSE_CONTENTS.content, 'html.parser')

    parsed_url = urlparse(request.get_url())
    scheme = parsed_url.scheme
    netloc = parsed_url.netloc

    for link in soup.find_all('link', href=True):
        rel = link.get("rel", None) 
        type_ = link.get("type", None)
        loc = link.get("href")
        module_logger.debug("Found <link> with href %s\n"
            "\tloc = %s\n"
            "\trel = %s\n"
            "\ttype = %s", link, loc, rel, type_)

        # content type css found
        if type_=="text/css" or "stylesheet" in rel:
            download(
                request_to_response,
                scheme,
                netloc,
                loc, 
                link, 
                content_handler.response_with_css_content_received
            )
            
    if download_img:
        for img in soup.find_all('img', src=True):
            download(
                request_to_response,
                scheme,
                netloc,
                img.get('src'), 
                img, 
                content_handler.response_with_img_content_received
            )
    
    if link_filter:
        for a in soup.find_all('a', href=True):

            if link_filter(a.get('href')):
                module_logger.debug("Found <a> with href %s", a)
                link = transform_url(
                    scheme, 
                    netloc, 
                    a.get('href')
                )

                scrap(
                    Request.from_url(link),
                    request_to_response,
                    content_handler,
                    download_img=download_img,
                    link_filter=link_filter,
                    max_level=max_level,
                    level=level+1
                )

    content_handler.html_post_process_handler(request, soup)

def webscraper(
    url, 
    request_to_response, 
    content_handler, 
    download_img=False,
    link_filter=None,
    max_level=1
):
    content_handler.session_started()

    scrap(
        Request.from_url(url),
        request_to_response,
        content_handler,
        download_img=download_img,
        link_filter=link_filter,
        max_level=max_level
    )
    content_handler.session_finished()
    
