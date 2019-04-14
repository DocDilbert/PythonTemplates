import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import time
# create logger
module_logger = logging.getLogger('webscraper')

class ExtractFileNameFromURL:
    def __init__(self, url, content_type):
        self.logger = logging.getLogger('webscraper.ExtractFileNameFromURL')
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
        self.logger = logging.getLogger('webscraper.WebScraperLogger')
        self.cnt = 0
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
        self.cnt += 1
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
        self.cnt += 1
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

#URL = "https://www.heise.de/newsticker/archiv/2006/01"
#URL = "https://www.spiegel.de/schlagzeilen/index-siebentage.html"
URL = "https://www.spiegel.de/sport/fussball/rsc-anderlecht-fans-erzwingen-spielabbruch-bei-standard-luettich-a-1262736.html"
#chrome 70.0.3538.77
HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def load_css(css_link, scraper):
    local = urlparse(css_link['href'])
    module_logger.debug("load css url_parse result = %s", local)
    o = urlparse(URL)
    page_link = o.scheme+"://"+o.netloc+css_link['href']
    module_logger.info("load css file from: %s", page_link)
    css = requests.get(page_link, headers=HEADERS)
    scraper.css_downloaded_handler(css_link, page_link, css)
    
def load_img(img_link, scraper):
    local = urlparse(img_link['src'])
    module_logger.debug("load_img url_parse result = %s", local)
    page_link = None
    if not local.scheme: 
        o = urlparse(URL)
        page_link = o.scheme+"://"+o.netloc+img_link['src']
    else:
        page_link = img_link['src']
    module_logger.info("load img file from: %s", page_link)
    img = requests.get(page_link, headers=HEADERS)
    scraper.img_downloaded_handler(img_link, page_link, img)
    

def main(scraper):
    page = requests.get(URL, headers=HEADERS)
    scraper.html_download_handler(URL, page)
    soup = BeautifulSoup(page.content, 'html.parser')

    for link in soup.find_all('link', {"type" : "text/css"}):
        load_css(link, scraper)

    for img in soup.find_all('img'):
        if img.get('src'):
            load_img(img, scraper)

    scraper.html_post_process_handler(URL, soup)
    

if __name__ == "__main__":
    logger_ = logging.getLogger('webscraper.ExtractFileNameFromURL')
    logger_.setLevel(logging.WARNING)

    logger_ = logging.getLogger('webscraper.WebScraperLogger')
    logger_.setLevel(logging.INFO)

    logger_ = logging.getLogger('webscraper')
    logger_.setLevel(logging.INFO)

    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger_.addHandler(ch)

    scraper = WebScraperLogger("page")
    main(scraper)