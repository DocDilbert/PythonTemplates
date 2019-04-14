import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
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
        self.logger = logging.getLogger('webscraper')
        self.cnt = 0
        self.dirname = dirname
        
        if not os.path.exists(dirname):
            os.mkdir(dirname)

    def html_pre_process_handler(self, url, page):
        self.logger.info("html pre process handler: %s", url)
        self.logger.debug("headers: %s", page.headers)
        self.logger.debug("cookies: %s", page.cookies)

        filename = ExtractFileNameFromURL(url, page.headers['Content-type'])
        with open(self.dirname+"/"+str(filename),"wb") as file:
            file.write(page.content)

    def css_downloaded_handler(self, tag, url, link_get):
        self.cnt += 1
        self.logger.info("css downloaded handler: %s", url)
        self.logger.debug("tag: %s", tag)
        self.logger.debug("headers: %s", link_get.headers)
        self.logger.debug("cookies: %s", link_get.cookies)
        
        filename = ExtractFileNameFromURL(url, link_get.headers['Content-type'])
        
        with open(self.dirname+"/"+str(filename),"wb") as file:
            file.write(link_get.content)

        tag['href'] = filename

    def html_post_process_handler(self, url, soup):
        
        self.logger.info("html post process handler: %s", url)
        
        filename = ExtractFileNameFromURL(url, "text/html; charset=utf-8")
        parts = os.path.splitext(str(filename))
        with open(self.dirname+"/{}_processed{}".format(parts[0], parts[1]),"w") as file:
            file.write(soup.prettify())

#URL = "https://www.heise.de/newsticker/archiv/2006/01"
URL = "https://www.spiegel.de/schlagzeilen/index-siebentage.html"

#chrome 70.0.3538.77
HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def load_css(css_link, scraper):
    o = urlparse(URL)
    page_link = o.scheme+"://"+o.netloc+css_link['href']
    css = requests.get(page_link, headers=HEADERS)
    scraper.css_downloaded_handler(css_link, page_link, css)
    

def main(scraper):
    page = requests.get(URL, headers=HEADERS)
    scraper.html_pre_process_handler(URL, page)
    soup = BeautifulSoup(page.content, 'html.parser')

    for link in soup.find_all('link', {"type" : "text/css"}):
        load_css(link, scraper)

    for img in soup.find_all('img'):
        print(img)

    scraper.html_post_process_handler(URL, soup)
    

if __name__ == "__main__":
    logger = logging.getLogger('webscraper.ExtractFileNameFromURL')
    logger.setLevel(logging.WARNING)

    logger = logging.getLogger('webscraper')
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    scraper = WebScraperLogger("page")
    main(scraper)