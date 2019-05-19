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
import pickle
import platform

# create logger
module_logger = logging.getLogger('webscraper.webscraper')


class Consumer(multiprocessing.Process):
    
    def __init__(self, task_queue, result_queue, request_to_response_factory):
        multiprocessing.Process.__init__(self)
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.request_to_response_factory = request_to_response_factory
        
    def run(self):
        request_to_response = self.request_to_response_factory.get()
        while True:
            next_task = self.task_queue.get()

            if next_task is None:
                # Poison pill means shutdown
                self.task_queue.task_done()
                break

            answer = next_task(request_to_response)

            self.result_queue.put(answer)
            self.task_queue.task_done()
    
        return


class Task(object):
    def __init__(self, url_history, request, type_):
        self.url_history = url_history
        self.request = request
        self.type_ = type_
        self.task_id = -1

    def __str__(self):
        return '{{task_id={}, type="{}", request={}, len(url_history)={}}}'.format(
            self.task_id, 
            self.type_,
            self.request,
            len(self.url_history)
        )

    def __repr__(self):
        return self.__str__()

    def __call__(self, request_to_response):

        response = request_to_response(self.request)
        return {
            'task_id' : self.task_id,
            'url_history' : self.url_history,
            'type_': self.type_,
            'request' : self.request,
            'response' : response
        }
    

class WebScraper:
    def __init__(self):
        self.logger = logging.getLogger('webscraper.webscraper.Webscraper')

    def transform_url(self, scheme, netloc, url):
        url_parsed = urlparse(url)
        self.logger.debug(
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

        self.logger.debug('Transform url from %s to %s', url, url_transf)

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
        add_task,
        url_history,
        download_img=False,
        link_filter=None,
    ):
        parsed_url = urlparse(request.get_url())
        scheme = parsed_url.scheme
        netloc = parsed_url.netloc

        tree = lxml.html.parse(BytesIO(response.content))
        content_handler.html_content_post_request_handler(request, response, tree)

        css = set()
        img = set()
        alist = set()

        root = tree.getroot()

        for (element, _, url, _) in root.iterlinks():

            if element.tag == "link":
                type_ = element.attrib.get('type', None)
                rel = element.attrib.get('rel', None)

                if not (type_ == "text/css" or "stylesheet" in rel):
                    continue
            
                #ignore duplicates
                if url in css:
                    continue

                self.logger.debug('Found <link> -> %s', url)
                css.add(url)

                url_transf = self.transform_url(scheme, netloc, url)
                request = Request.from_url(url_transf)
                content_handler.css_content_pre_request_handler(
                    request,
                    element,
                )
                new_url_history = list(url_history)
                new_url_history.append(url)
                add_task(Task(
                    new_url_history,
                    request,
                    'CSS'
                ))

            if element.tag == "img":
                if 'src' not in element.attrib:
                    continue

                src = element.attrib.get('src')

                if 'data:image/' in src:
                    continue  # img was embedded

                #ignore duplicates
                if url in img:
                    continue

                self.logger.debug('Found <img> -> %s', url)
                img.add(url)

                if download_img:
                    url_transf = self.transform_url(scheme, netloc, url)
                    request = Request.from_url(url_transf)
                    content_handler.img_content_pre_request_handler(
                        request,
                        element,
                    )
                    new_url_history = list(url_history)
                    new_url_history.append(url)
                    add_task(Task(
                        new_url_history,
                        request,
                        'IMG',
                    ))


            if element.tag == "a":
                if 'href' not in element.attrib:
                    continue

                #ignore duplicates
                if url in alist:
                    continue
                
                self.logger.debug('Found <a> -> %s', url)

                alist.add(url)

                if link_filter:
                    if link_filter(url, url_history):
                        self.logger.debug(
                            "Filter accepted url \"%s\"", url)

                        url_transf = self.transform_url(
                            scheme,
                            netloc,
                            url
                        )
                        request = Request.from_url(url_transf)
                        new_url_history = list(url_history)
                        new_url_history.append(url)
                        add_task(Task(
                            new_url_history,
                            request,
                            'HTML'
                        ))
                    else: 
                        self.logger.debug(
                            "Filter denied url \"%s\"", url)
                
        content_handler.html_content_post_process_handler(request, tree)

    def webscraper(
        self,
        url,
        request_to_response_factory,
        content_handler,
        download_img=False,
        link_filter=None
    ):
        content_handler.session_started()
        tasks = multiprocessing.JoinableQueue()
        results = multiprocessing.Queue()

        # Start consumers

        if platform.system() == "Windows":
            num_consumers = multiprocessing.cpu_count() * 2 #4
        else:
            num_consumers = multiprocessing.cpu_count() * 2

        self.logger.info('Creating %d consumers', num_consumers)

        
        consumers=[]
        for idx in range(num_consumers):
            self.logger.debug('Create consumer %d', idx)
            consumer = Consumer(
                tasks, 
                results, 
                request_to_response_factory
            )

            consumers.append(consumer)

        for idx,w in enumerate(consumers):
            self.logger.info('Start consumer %d', idx)
            w.start()
            
        task_set = set()
        class AddTask:
            def __init__(self, logger):
                self.task_id = 0
                self.logger = logger

            def __call__(self, task): 
                
                task.task_id = self.task_id

                
                task_set.add(self.task_id)
                self.task_id+=1
                tasks.put(task)
                self.logger.info("Task added: %s", task)  

        add_task = AddTask(self.logger)
        add_task( Task(
            [], # no history 
            Request.from_url(url),
            'HTML'
        ))

        while(len(task_set) != 0):
            to_download = results.get(block=True)

            # keep track how much task are running
            task_set.remove(to_download['task_id'])

            type_ = to_download['type_']
            url_history = to_download['url_history']
            request = to_download['request']
            response = to_download['response']

            self.logger.info('Task {"task_id":%i, "type":"%s"} finished.', to_download['task_id'], type_) 
            self.logger.debug("Task response: %s", response) 

            if (type_ == 'HTML'):
                self.process_html(
                    request,
                    response,
                    content_handler,
                    add_task=add_task,
                    url_history=url_history,
                    download_img=download_img,
                    link_filter=link_filter
                )

            elif (type_ == 'IMG'):
                content_handler.img_content_post_request_handler(request, response)
            elif (type_ == 'CSS'):
                content_handler.css_content_post_request_handler(request, response)
            else:
                raise Exception()

        # Add a poison pill for each consumer
        for _ in range(num_consumers):
            tasks.put(None)

        # Wait for all of the tasks to finish
        tasks.join()

        content_handler.session_finished()
