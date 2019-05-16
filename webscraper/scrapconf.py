import logging
import logging.handlers as handlers
from urllib.parse import urlparse, urlunparse


LOGDIR = "log/"
LOGTYPE = "single"
LOGFILE_DEBUG = "webscraper.log"
LOGFILE_ERRORS = "webscraper_errors.log"

DATABASE_DIR  = "data/"
DATABASE = "webscraper.db"

URL =  ("https://www.stepstone.de/5/ergebnisliste.html?"
       "fu=10012000%2C10006000%2C10007000%2C10002000%2C10022000%2C10013000%2C10014000%2C10015000%2C10020000%2C10011000%2C10017000%2C10016000%2C10009008%2C10004000%2C10005000%2C10009007%2C10018000%2C10024000%2C10010005%2C10019000%2C10008000%2C10009010%2C10021000%2C10009001%2C10009005%2C10001000%2C10009009%2C10023000%2C10009006%2C10010000&"
       "fre=200000096&an=facets&li=100&wt=80001&ct=222&fu=1000000&fid=1000000&fn=categories&fa=select")


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
    logger3.setLevel(logging.INFO)

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
        self.occurences = 0
        self.max_depth = -1
        self.max_occurences = 100

    def filter(self, url, depth):
        #self.logger.info(urlparse(x))
        ( _scheme, 
           _netloc, 
           _path, 
           _params,
           query, 
           _fragment
        ) = urlparse(url)

        queries = query.split("&")
        
        if ("an=paging%5Fnext" in queries) or ("action=paging_next" in queries):
            self.occurences = self.occurences + 1

            if (self.max_occurences == -1) or (self.occurences <= self.max_occurences):

                if (self.max_depth != -1) and (depth >= self.max_depth):
                    self.logger.debug("Denied (too deep) \"%s\"", url)
                    return False
                else:
                    self.logger.debug("Link accepted \"%s\"", url)
                    return True
            else:
                self.logger.debug(
                    "Link denied (too much much occurences) \"%s\"", url)
                return False

        self.logger.debug("Link denied (no regex match) \"%s\"", url)
        return False
