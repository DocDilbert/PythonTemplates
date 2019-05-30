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
    (
        "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159096",
        {
            "root" : True
        }
    ), # DAX
    (
        "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159090",
        {
            "root" : True           
        }
    ), # MDAX
    (
        "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=158375",
        {
            "root" : True             
        }
    ), # TECDAX
    (
        "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159191",
        {
            "root" : True             
        }
    ), # SDAX
    (
        "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159194",
        {
            "root" : True   
        }
    ), # EUROSTOXX50
    (
        "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=159196",
        {
            "root" : True 
        }
    ), # Stoxx Europe 50
    (
        "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=849973",
        {
            "root" : True 
        }
    ), # Dow Jones
    (
        "https://kurse.boerse.ard.de/ard/indizes_einzelkurs_uebersicht.htn?i=149002",
        {
            "root" : True    
        }
    ), # Nasdaq 100
    (
        "https://kurse.boerse.ard.de/ard/etf_einzelkurs_uebersicht.htn?i=320389",
        {
            "content" : True
        } 
    ), #LU0392494562
    (
        "https://kurse.boerse.ard.de/ard/etf_einzelkurs_uebersicht.htn?i=104171",
        {
            "content" : True
        } 
    ), # DE0006289473
    (
        "https://kurse.boerse.ard.de/ard/etf_einzelkurs_uebersicht.htn?i=20562180",
        {
            "content" : True
        } 
    ), # IE00B0M63177
    (
        "https://kurse.boerse.ard.de/ard/etf_einzelkurs_uebersicht.htn?i=2562488",
        {
            "content" : True
        } 
    ) # DE000A0H0728

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
        self.einzelkurs_regex = re.compile(r"https:\/\/.*\/kurse_einzelkurs_uebersicht\.htn\?i\=\d*$")
        self.history_regex =  re.compile(r"https:\/\/.*\/kurse_einzelkurs_history\.htn\?i\=\d*$")
        self.profil_regex =  re.compile(r"https:\/\/.*\/kurse_einzelkurs_profil\.htn\?i\=\d*$")
        self.etf_portrait = re.compile(r"https:\/\/.*\/etf_einzelkurs_uebersicht\.htn\?i\=\d+&sektion=gesamtportrait$")
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

    def filter(self, url, url_history, meta):
        #self.logger.info(urlparse(x))

        if url in self.visited:
            return False, {}

        # Check if further pages exist in list
        if meta.get('root', False):
            
            if self.check_next_page(url):
                self.visited.add(url)
                return True, {'next_page' : True}
            
            if self.einzelkurs_regex.match(url):
                self.visited.add(url)
                return True, {'content': True}

        if meta.get('next_page', False):
            if self.check_next_page(url):
                self.visited.add(url)
                return True, {'next_page' : True}

            if self.einzelkurs_regex.match(url):
                self.visited.add(url)
                return True, {'content': True}

        # Wurde eine Uebersicht geholt?
        if meta.get('content', False):
            
            # dann überprüfe auf history link
            if self.history_regex.match(url):
                self.visited.add(url)
                return True, {}
                
            # oder profil link
            if self.profil_regex.match(url):
                self.visited.add(url)
                return True, {}

            # oder etf portrait link
            if self.etf_portrait.match(url):
                self.visited.add(url)
                return True, {}


        return False, {}
