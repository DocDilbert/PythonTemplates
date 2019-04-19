import logging
import webscraper.webscraper as webscraper 
from webscraper.content_handler_sqlite import ContentHandlerSqlite
from webscraper.content_handler_logger import ContentHandlerLogger
from webscraper.content_handler_filesystem import ContentHandlerFilesystem
from urllib.parse import urlparse,urlunparse
import os

#URL = "https://www.heise.de/newsticker/archiv/2006/01"
#URL = "https://www.spiegel.de/schlagzeilen/index-siebentage.html"
URL = "http://store.total.de/de_DE/ND001552"
#URL = "https://www.spiegel.de/sport/fussball/rsc-anderlecht-fans-erzwingen-spielabbruch-bei-standard-luettich-a-1262736.html"


def main():
    logger = logging.getLogger('webscraper')
    logger.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    fh = logging.FileHandler('webscraper.log', mode='w')
    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s]: %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info("-------------------------------------")
    logger.info(" Web scrapper session startet")
    logger.info("-------------------------------------")

    content_handler = ContentHandlerFilesystem("page")
    content_handler_logger = ContentHandlerLogger()
    content_handler_sqlite = ContentHandlerSqlite("requests.db")

    content_handler_sqlite.set_component(content_handler_logger)
    content_handler.set_component(content_handler_sqlite)

    links = webscraper.scrap(URL, content_handler, download_img=True)

    for link in links:
        parts=urlparse(link)
        filename = os.path.basename(parts.path)
        filen = os.path.splitext(filename)

        if filen[1]==".html":
            print(link)
            #scrap(link, scraper)

if __name__ == "__main__":
    main()