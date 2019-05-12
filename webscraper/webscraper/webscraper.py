# -*- coding: utf-8 -*-

import requests
import logging
import os
import time
import string
from urllib.parse import urlparse, urlunparse


from webtypes.request import Request
from webtypes.response import Response
import lxml.html
from io import StringIO, BytesIO
import pprint

from collections import deque
import multiprocessing

# chrome 70.0.3538.77
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

# create logger
module_logger = logging.getLogger('webscraper.webscraper')

class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        proc_name = self.name
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                # Poison pill means shutdown
                print('%s: Exiting' % proc_name)
                self.task_queue.task_done()
                break

            print('%s: %s' % (proc_name, next_task))
            answer = next_task()
            self.result_queue.put(answer)
            self.task_queue.task_done()
        return


class Task(object):
    def __init__(self, depth, url, type_):
        self.depth = depth
        self.url = url
        self.type_ = type_

    def __call__(self):
        return {
            'depth' : self.depth,
            'url' : self.url,
            'type' : self.type_
        }
    

class WebScraper:
    def transform_url(self, scheme, netloc, url):
        url_parsed = urlparse(url)
        module_logger.debug(
            'Transform url with url_parse results in = %s', url_parsed)

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

            if element.tag == "link":
                type_ = element.attrib.get('type', None)
                rel = element.attrib.get('rel', None)

                if type_ == "text/css" or "stylesheet" in rel:
                    module_logger.debug('Found <link> -> %s', link)
                    css[link] = element

                

            if element.tag == "img":
                if 'src' not in element.attrib:
                    continue

                src = element.attrib.get('src')

                if 'data:image/' in src:
                    continue  # img was embedded

                module_logger.debug('Found <img> -> %s', link)
                img[link] = element

            if element.tag == "a":
                if 'href' not in element.attrib:
                    continue

                module_logger.debug('Found <a> -> %s', link)
                alist[link] = element

        parsed_url = urlparse(request.get_url())
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc

        tasks = []

        # CSS HANDLING
        for link, element in css.items():
            url_transf = self.transform_url(scheme, netloc, link)
            request = Request.from_url(url_transf)
            content_handler.css_content_pre_request_handler(
                request,
                element,
            )

            tasks.append(Task(
                depth+1,
                url_transf,
                'CSS'
            ))

        # IMG HANDLING
        if download_img:
            for link, element in img.items():
                url_transf = self.transform_url(scheme, netloc, link)
                request = Request.from_url(url_transf)
                content_handler.img_content_pre_request_handler(
                    request,
                    element,
                )

                tasks.append(Task(
                    depth+1,
                    url_transf,
                    'IMG',
                ))

        download_links = set()
        if link_filter:
            for link,_  in alist.items():
                if link_filter(link, depth):
                    module_logger.info(
                        "Filter accepted link to new page \"%s\"", link)

                    link = self.transform_url(
                        scheme,
                        netloc,
                        link
                    )
                    download_links.add(link)

        tasks += (Task(
            depth+1,
            link,
            'HTML'
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
        tasks = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()

        # Start consumers
        num_consumers = multiprocessing.cpu_count() * 2
        print('Creating %d consumers' % num_consumers)
        consumers = [ Consumer(tasks, results)
                    for i in range(num_consumers) ]
        for w in consumers:
            w.start()

        tasks.put(Task(
            0, 
            url,
            'HTML'
        ))

        while(1):

            to_download = results.get()

            type_ = to_download['type']
            url = to_download['url']
            depth = to_download['depth']

            request = Request.from_url(url)
            response = request_to_response(request)

            if (type_ == 'HTML'):
                new_tasks = self.process_html(
                    request,
                    response,
                    content_handler,
                    depth=depth,
                    download_img=download_img,
                    link_filter=link_filter
                )
                for i in new_tasks:
                    tasks.put(i)

            elif (type_ == 'IMG'):
                content_handler.img_content_post_request_handler(request, response)
            elif (type_ == 'CSS'):
                content_handler.css_content_post_request_handler(request, response)
            else:
                raise Exception()

            if (tasks.empty()) and (results.empty()):

                # Wait for all of the tasks to finish
                tasks.join()

                if (tasks.empty()) and (results.empty()):
                    break

        # Add a poison pill for each consumer
        for i in range(num_consumers):
            tasks.put(None)

        # Wait for all of the tasks to finish
        tasks.join()

        content_handler.session_finished()
