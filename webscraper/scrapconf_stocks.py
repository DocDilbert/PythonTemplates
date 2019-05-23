import logging
import logging.handlers as handlers
from urllib.parse import urlparse, urlunparse
import re

LOGDIR = "log/"
LOGTYPE = "single"
LOGFILE_DEBUG = "webscraper.log"
LOGFILE_ERRORS = "webscraper_errors.log"

DATABASE_DIR  = "data_stocks/"
DATABASE = "webscraper.db"

DOWNLOAD_IMGS = False
SLEEP_TIME = 1.0
URLS =  [
    ("https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159096"), #DAX
    ("https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159090"), #MDAX
    ("https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=158375"), #TECDAX
    ("https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159191"), #SDAX
    ("https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159194"), #EUROSTOXX50
    ("https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159196"), #Stoxx Europe 50
]


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
        self.einzelkurs_regex = re.compile(r"\/.*\/kurse_einzelkurs_uebersicht\.htn")
        self.history_regex =  re.compile(r"\/.*\/kurse_einzelkurs_history\.htn")
        self.profil_regex =  re.compile(r"\/.*\/kurse_einzelkurs_profil\.htn")

        self.visited = set()
    def check_next_page(self, url):

        up = urlparse(url)
        queries = up.query.split("&")
        
        if "sortierung=descriptionShort" not in queries:
            return False
        if "offset=0" in queries:
            return False
        if "ascdesc=ASC"  not in queries:
            return False

        for q in queries:
            if "offset=" in q:
                return True

        return False

    def filter(self, url, url_history):
        #self.logger.info(urlparse(x))
        up = urlparse(url)
        path = up.path
    
        if url in self.visited:
            return False

       
        last_url = url_history[-1]
        
        # Check if further pages exist in list
        if self.check_next_page(last_url) or len(url_history)==1:
            if self.check_next_page(url):
                self.visited.add(url)
                return True

            if self.einzelkurs_regex.match(path):
                self.visited.add(url)
                return True

        last_path = urlparse(last_url).path

        # Wurde eine Uebersicht geholt?
        if self.einzelkurs_regex.match(last_path):
            # dann überprüfe auf history link
            if self.history_regex.match(path):
                self.visited.add(url)
                return True
            # oder profil link
            if self.profil_regex.match(path):
                self.visited.add(url)
                return True

        return False
