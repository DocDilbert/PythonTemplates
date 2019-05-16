import webscraper
import sys
import logging
from webscraper.command_line_parser import WebScraperCommandLineParser
from cProfile import Profile

ENABLE_CPROFILE = True
# create logger
module_logger = logging.getLogger('webscraper.__main__')

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    module_logger.exception("Uncaught exception", exc_info=(
        exc_type, exc_value, exc_traceback))



def main(argv):
     # Install exception handler
    sys.excepthook = handle_exception
    if ENABLE_CPROFILE:
        prof = Profile()
        prof.enable()
    WebScraperCommandLineParser(argv)

    if ENABLE_CPROFILE:
        prof.disable()  # don't profile the generation of stats
        prof.dump_stats('webscraper.prof')

if __name__ == "__main__":
    main(sys.argv)
