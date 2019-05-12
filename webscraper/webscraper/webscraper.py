# -*- coding: utf-8 -*-

import requests
import logging
import os
import time
import string
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse


from webtypes.request import Request
from webtypes.response import Response
import lxml.html
from io import StringIO, BytesIO
import pprint

from collections import deque


#chrome 70.0.3538.77
HEADERS = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

# create logger
module_logger = logging.getLogger('webscraper.webscraper')

class WebScraper:
    def transform_url(self, scheme, netloc, url):
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

    def is_internal(self, netloc, url):
        url_parsed = urlparse(url)

        if url_parsed.netloc == netloc:
            return True
        else:
            return False
            

    def process_html(
        self,
        request,
        response, 
        request_to_response, 
        content_handler, 
        depth,
        download_img=False,
        link_filter=None,
    ):
        
        tree = lxml.html.parse(BytesIO(response.content))
        content_handler.html_content_post_request_handler(request, response, tree)

        css = dict()
        img = dict()
        alist = dict()
        for (element, _, link, _) in tree.getroot().iterlinks():

            if element.tag=="link":
                type_ = element.attrib.get('type', None)
                rel = element.attrib.get('rel', None)
                
                if type_=="text/css" or "stylesheet" in rel:
                    css[link] = element

            if element.tag=="img":
                if 'src' not in element.attrib:
                    continue

                src = element.attrib.get('src')

                if 'data:image/' in src:
                    continue # img was embedded

                img[link] = element      

            if element.tag=="a":
                if 'href' not in element.attrib:
                    continue     

                alist[link] = element 


        parsed_url = urlparse(request.get_url())
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc

        tasks = []
        for link, element in css.items():

            module_logger.debug("Found <link> -> %s",link)

            url_transf = self.transform_url(scheme, netloc, link)
            request = Request.from_url(url_transf)
            content_handler.css_content_pre_request_handler(
                request,
                element,
            )

            tasks.append((
                    url_transf,
                    lambda request, response: 
                        content_handler.css_content_post_request_handler(request, response)
                    )
                )

        if download_img:
            for link, element in img.items():

                url_transf = self.transform_url(scheme, netloc, link)
                request = Request.from_url(url_transf)
                content_handler.img_content_pre_request_handler(
                    request,
                    element,
                )

                
                tasks.append((
                    url_transf,
                    lambda request, response: 
                        content_handler.img_content_post_request_handler(request, response)
                    )
                )

        found_links = set()
        for link, element in alist.items():
            module_logger.debug('Found <a> -> %s', link)
            found_links.add(link)

        download_links = set()
        if link_filter:
            for link in found_links:
                if link_filter(link, depth):
                    module_logger.info("Filter accepted link to new page \"%s\"", link)
                    link = self.transform_url(
                        scheme, 
                        netloc, 
                        link
                    )
                    download_links.add(link)
        tasks+= ((
                    link,
                    lambda request, response: self.process_html(
                        request,
                        response,
                        request_to_response,
                        content_handler,
                        depth = depth + 1,
                        download_img=download_img,
                        link_filter=link_filter
                    )
                ) for link in download_links)
        
        content_handler.html_content_post_process_handler(request, tree)

        return tasks          

    def webscraper(
        self,
        url, 
        request_to_response, 
        content_handler, 
        download_img=False,
        link_filter=None,
        max_level=1
    ):

        content_handler.session_started()

        download_queue = deque([
            (
                url,
                lambda request, response: self.process_html(
                    request,
                    response,
                    request_to_response,
                    content_handler,
                    depth = 0,
                    download_img=download_img,
                    link_filter=link_filter
                )
            )
        ])
   
        while(len(download_queue) != 0):
            to_download = download_queue.popleft()

            request = Request.from_url(
                to_download[0]
            )
            response = request_to_response(request) 

            task = to_download[1]

            new_downloads = task(
                request,
                response
            )
            
            if new_downloads:
                for i in new_downloads:
                    download_queue.append(i)
 
        content_handler.session_finished()
        
