import logging
import logging.handlers as handlers
from urllib.parse import urlparse, urlunparse
import re

LOGDIR = "log/"
LOGTYPE = "single"
LOGFILE_DEBUG = "webscraper.log"
LOGFILE_ERRORS = "webscraper_errors.log"

DATABASE_DIR  = "data/"
DATABASE = "webscraper.db"

DOWNLOAD_IMGS = False

SLEEP_TIME = 1.0
URL =  ("https://www.stepstone.de/5/ergebnisliste.html?fu=10012000%2C10006000%2C10007000%2C10002000%2C10022000%2C10013000%2C10014000%2C10015000%2C10020000%2C10011000%2C10017000%2C10016000%2C10009008%2C10004000%2C10005000%2C10009007%2C10018000%2C10024000%2C10010005%2C10019000%2C10008000%2C10009010%2C10021000%2C10009001%2C10009005%2C10001000%2C10009009%2C10023000%2C10009006%2C10010000&fre=200000096&an=facets&li=100&wt=80001&ct=222&fu=1000000&fid=1000000&fn=categories&fa=select")


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
        self.offer_regex = re.compile(r'\/stellenangebote--.*')

    def filter(self, url, url_history):
        #self.logger.info(urlparse(x))
        ( _scheme, 
           _netloc, 
           path, 
           _params,
           query, 
           _fragment
        ) = urlparse(url)

        queries = query.split("&")
        
        #if (len(url_history)>=2):
        #   return False

        if (len(url_history)>=1):

            ( _, _, last_path, _,_, _
            ) = urlparse(url_history[-1])
            # don't follow links on offer sites
            if self.offer_regex.match(last_path):
                return False

        if (self.offer_regex.match(path)):
            return True
        if ("an=paging%5Fnext" in queries) or ("action=paging_next" in queries):
            return True
        else:
            return False
