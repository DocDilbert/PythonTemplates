import logging
import logging.handlers as handlers
from urllib.parse import urlparse, urlunparse
import re

LOGDIR = "log/"
LOGTYPE = "single"
LOGFILE_DEBUG = "webscraper.log"
LOGFILE_ERRORS = "webscraper_errors.log"

DATABASE_DIR  = "data_dax/"
DATABASE = "webscraper.db"

DOWNLOAD_IMGS = False
SLEEP_TIME = 1.0
URL =  ("https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159096")


def init_logger():
    if LOGTYPE == "rotate":
        fh = handlers.RotatingFileHandler(
            LOGDIR + LOGFILE_DEBUG,
            maxBytes=10*1024*1024,
            backupCount=10
        )
    else:
        fh = logging.FileHandler(
            LOGDIR + LOGFILE_DEBUG,
            mode='w',
            encoding="utf-8"
        )

    # fh.setLevel(logging.DEBUG)

    fh.setLevel(logging.DEBUG)

    eh = logging.FileHandler(
        LOGDIR + LOGFILE_ERRORS,
        delay=True,
        encoding="utf-8"
    )
    eh.setLevel(logging.ERROR)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s [%(name)s]: %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    eh.setFormatter(formatter)

    logger = logging.getLogger('webscraper')
    logger.setLevel(logging.INFO)

    logger2 = logging.getLogger('webdb')
    logger2.setLevel(logging.INFO)

    logger3 = logging.getLogger('scrapconf')
    logger3.setLevel(logging.DEBUG)

    logger.addHandler(fh)
    logger.addHandler(ch)
    logger.addHandler(eh)

    logger2.addHandler(fh)
    logger2.addHandler(ch)
    logger2.addHandler(eh)

    logger3.addHandler(fh)
    logger3.addHandler(ch)
    logger3.addHandler(eh)


class LinkFilter:
    def __init__(self):
        self.logger = logging.getLogger('scrapconf.LinkFilter')
        self.einzelkurs_regex = re.compile(r"\/.*\/kurse_einzelkurs_uebersicht\.htn")
        self.history_regex =  re.compile(r"\/.*\/kurse_einzelkurs_history\.htn")
    def filter(self, url, url_history):
        #self.logger.info(urlparse(x))
        (   scheme, 
            netloc, 
            path, 
            params,
            query, 
            fragment
        ) = urlparse(url)

        if len(url_history)==0:
            if self.einzelkurs_regex.match(path):
                return True
        elif len(url_history)==1:
            if self.history_regex.match(path):
                return True
        return False
